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
    '''RoyalChaos - Tools made by JSimo'''
    pass

@main.command()
@click.option('--name', prompt='Container name?')
def start(name):
    '''Start to monitor container with given name'''
    container_name = name
    container = docker_client.containers.get(container_name)
    monitoring.startMonitoring(container)

@main.command()
@click.option('--name', prompt='Container name?')
def stop(name):
    '''Stop to monitor container with given name'''
    container_name = name
    container = docker_client.containers.get(container_name)
    monitoring.stopMonitoring(container)

@main.command()
def list():
    '''List all containers relevant to royal currently running'''
    containers = docker_client.containers.list(
        filters={'name': 'se.kth.royalchaos'})
    print([c.name for c in containers])

if __name__ == '__main__':
    main()
