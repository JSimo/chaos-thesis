import os
import time

# Package imports
import click
import docker

# Local imports
import monitoring


# Create docker client
docker_client = docker.from_env()

@click.group()
def main():
    """main"""
    pass

@main.command()
@click.option("--name", prompt="Container name?")
def start(name):
    container_name = name
    container = docker_client.containers.get(container_name)
    monitoring.startMonitoring(container)

@main.command()
@click.option("--name", prompt="Container name?")
def stop(name):
    container_name = name
    container = docker_client.containers.get(container_name)
    monitoring.stopMonitoring(container)

#def main():
#    print('Hello world')
#    if not 'RORC_TEST' in os.environ:
#        print('Missing required environment variable \"RORC_TEST\"')
#        exit(1)
#    elif 'CLEANUP' in os.environ and os.environ['CLEANUP'] == "true":
#        container_name = os.environ['RORC_TEST']
#        container = docker_client.containers.get(container_name)
#        monitoring.stopMonitoring(container)

if __name__ == '__main__':
    main()
