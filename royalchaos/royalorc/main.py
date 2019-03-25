import os
import time

# Package imports
import click
import docker

# Local imports
import monitoring
import prometheus_api

# Create docker client
docker_client = docker.from_env()

@click.group()
def main():
    '''RoyalChaos - Tool made by JSimo'''
    pass

@main.command()
@click.option('--name', prompt='Container name?')
def start(name):
    '''Start to monitor container with given name'''
    container = getContainer(name)
    monitoring.startMonitoring(container)

@main.command()
@click.option('--name', prompt='Container name?')
def stop(name):
    '''Stop to monitor container with given name'''
    container = getContainer(name)
    monitoring.stopMonitoring(container)

@main.command()
def list():
    '''List all containers relevant to royal currently running'''
    containers = docker_client.containers.list(
        filters={'name': 'se.kth.royalchaos'})
    print([c.name for c in containers])

@main.command()
def m():
    print(prometheus_api.testQuery())

def getContainer(name):
    '''Returns a container of given name and prints error message if does not exist.'''
    try:
        return docker_client.containers.get(name)
    except docker.errors.NotFound:
        print('Container with name "%s" not found' % name)
        exit()

if __name__ == '__main__':
    main()
