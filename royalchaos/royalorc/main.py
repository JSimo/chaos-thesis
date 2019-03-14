import docker
import os
import time

# Local imports
import prometheus

# Create docker client
docker_client = docker.from_env()
docker_api_client = docker.APIClient(base_url='unix://var/run/docker.sock')

# Temporary global variables
monitoring_network_name = 'royalnetm_back-tier'

def getIpFromContainerAttachedNetwork(container, network_name):
    return container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']

def getIpFromContainer(container):
    return container.attrs['NetworkSettings']['IPAddress']

def main():
    print('Hello world')
    if not 'RORC_TEST' in os.environ:
        print('Missing required environment variable \"RORC_TEST\"')
        exit(1)
    else:
        container_name = os.environ['RORC_TEST']
        container = docker_client.containers.get(container_name)
        startMonitoring(container)

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
        name='jsimo2.royalnetm.'+container_name,
        network_mode='container:'+container_name))
    print("Launched network container with IP", container_ip)

    #1.1 Connect prometheus to container and get IP.
    # This as we can't access it container to container.
    docker_client.networks.get(monitoring_network_name).connect(container_name)
    container.reload() # REFRESH container variable with new IPAddress content.
    container_monit_ip = getIpFromContainerAttachedNetwork(container, monitoring_network_name)

    #1.2 Adds network monitoring container as a prometheus target.
    prometheus.addTarget(container_monit_ip + ':12301', container_name)
    print("Added network monitoring with ip:", container_monit_ip)

    #2. Launch syscall monitoring utilizing the same process namespace.
    #docker_client.containers.run(
    #   'jsimo2/royalsysm',
    #   detach=True,
    #   pid_mode="container:"+container_name)

    #3. Verify monitoring, maybe send something on the open port? :hm:

    #4. Report ready for perturbations.

    pass

if __name__ == '__main__':
    main()
