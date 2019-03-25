import os
import time

# Package improts
import click
import docker

# Local imports
import monitoring


# Create docker client
docker_client = docker.from_env()

#@click.group()
#def main():
#    """main"""
#    pass

def main():
    print('Hello world')
    if not 'RORC_TEST' in os.environ:
        print('Missing required environment variable \"RORC_TEST\"')
        exit(1)
    elif 'CLEANUP' in os.environ and os.environ['CLEANUP'] == "true":
        container_name = os.environ['RORC_TEST']
        container = docker_client.containers.get(container_name)
        monitoring.stopMonitoring(container)
    else:
        container_name = os.environ['RORC_TEST']
        container = docker_client.containers.get(container_name)
        monitoring.startMonitoring(container)

if __name__ == '__main__':
    main()
