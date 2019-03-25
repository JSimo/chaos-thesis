
# Package import
import docker

# Local import
import prometheus

docker_client = docker.from_env()

# Temporary global variables
monitoring_network_name = 'royalnetm_back-tier'
base_name = 'jsimo2'
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
        name='jsimo2.netm.'+container_name,
        network_mode='container:'+container_name,
        remove=True
        ))
    print("Launched network container with IP", container_ip)

    #1.1 Connect prometheus to container and get IP.
    # This as we can't access it container to container.
    docker_client.networks.get(monitoring_network_name).connect(container_name)
    container.reload() # REFRESH container variable with new IPAddress content.
    container_monit_ip = getIpFromContainerAttachedNetwork(container, monitoring_network_name)

    #1.2 Adds network monitoring container as a prometheus target.
    prometheus.addTarget(container_monit_ip + ':12301', container_name) #TODO refactor port.
    print("Added network monitoring with ip:", container_monit_ip)

    #2. Launch syscall monitoring utilizing the same process namespace.
    #docker_client.containers.run(
    #   'jsimo2/royalsysm',
    #   detach=True,
    #   pid_mode="container:"+container_name)

    #3. Verify monitoring, maybe send something on the open port? :hm:

    #4. Report ready for perturbations.
    pass

def stopMonitoring(container):
    '''Cleanup after'''
    container_name = container.name

    #1. Stop network monitoring.
    docker_client.containers.get(base_name_netm + '.' + container_name).kill() #stop()
    #1.1 Disconnect container from network.
    docker_client.networks.get(monitoring_network_name).disconnect(container_name)

    #2. Stop syscall monitoring.

    #3. Remove from prometheus discovery.
    prometheus.removeTarget(container_name)

