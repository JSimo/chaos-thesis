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

if __name__ == '__main__':
    main()
