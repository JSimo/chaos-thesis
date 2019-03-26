import requests
import time

# Package import
import docker

# Local import
import prometheus

docker_client = docker.from_env()

# Temporary global variables
monitoring_network_name = 'royalchaos_back-tier'
base_name = 'se.kth.royalchaos'
base_name_netm = base_name + '.netm'
base_name_sysm = base_name + '.sysm'

def getIpFromContainerAttachedNetwork(container, network_name):
    return container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']

def getIpFromContainer(container):
    return container.attrs['NetworkSettings']['IPAddress']

# Launches the monitoring sidecars for the docker container.
def startMonitoring(container):
    # Variables:
    container_name = container.name
    container_ip = getIpFromContainer(container)

    #1. Launch network monitoring utilizing the same networking namespace/stack.
    print(docker_client.containers.run(
        'jsimo2/royalnetm',
        detach=True,
        environment=['ROYALNETM_IP='+container_ip],
        name=base_name_netm+'.'+container_name,
        network_mode='container:'+container_name,
        remove=True
        ))

    print("Launched network container with IP", container_ip)

    #1.1. Connect prometheus to container and get IP.
    # This as we can't access it container to container.
    docker_client.networks.get(monitoring_network_name).connect(container_name)
    container.reload() # REFRESH container variable with new IPAddress content.
    container_monit_ip = getIpFromContainerAttachedNetwork(container, monitoring_network_name)

    #1.2. Adds network monitoring container as a prometheus target.
    prometheus.addTarget(container_monit_ip + ':12301', container_name) #TODO refactor port.
    print("Added network monitoring with ip:", container_monit_ip)

    #2. Launch syscall monitoring utilizing the same process namespace.
    sysm_container = docker_client.containers.run(
        'jsimo2/royalsysm',
        cap_add=['SYS_PTRACE'],
        detach=True,
        environment=['SYSM=6'], #TODO do not hardcode PID
        name=base_name_sysm+'.'+container_name,
        pid_mode="container:"+container_name,
        remove=True)
    #2.1. Connect prometheus to contaiener.
    docker_client.networks.get(monitoring_network_name).connect(sysm_container)

    #2.2. Adds system call monitoring to prometheus targets.
    sysm_container.reload()
    sysm_container_ip = getIpFromContainerAttachedNetwork(sysm_container, monitoring_network_name)
    prometheus.addTarget(sysm_container_ip + ':12301', container_name)

    #3. Wait for monitoring to be up.
    monitor_ips = [container_monit_ip, sysm_container_ip]
    for ip in monitor_ips:
        waitForMonitoring('http://%s:12301' % ip)

    #4. Print container ports. Maybe do something to send request, and then check monitoring to verify working.
    container_ports = container.attrs['NetworkSettings']['Ports']
    #print(container_ports)
    for inside_port in container_ports:
        for outside in container_ports[inside_port]:
            print('open port', outside['HostPort'])
            # Ignore return value, just to send traffic to verify monitoring working.
            print(requests.get(url='http://localhost:'+outside['HostPort']))

    #5. Report ready for perturbations.
    pass

def stopMonitoring(container):
    '''Cleanup after'''
    container_name = container.name

    #1. Stop network monitoring.
    docker_client.containers.get(base_name_netm+'.'+container_name).kill() #stop()
    #1.1 Disconnect container from prometheus network.
    docker_client.networks.get(monitoring_network_name).disconnect(container_name)

    #2. Stop syscall monitoring.
    docker_client.containers.get(base_name_sysm+'.'+container_name).kill() #stop()
    #2.1 Disconnect container from prometheus network.
    docker_client.networks.get(monitoring_network_name).disconnect(base_name_sysm+'.'+container_name)

    #3. Remove from prometheus discovery.
    prometheus.removeTarget(container_name)

def waitForMonitoring(address):
    '''Recursively waits for address to be up'''
    # TODO: Can get stuck here if the address does not exist, rewrite to handle this.
    print('.', end='')
    try:
        requests.get(address)
        print('monitoring is up!')
    except Exception:
        # try again
        time.sleep(0.05)
        waitForMonitoring(address)
