import docker

def getClient():
    return docker.from_env()

def ls():
    """List all containers by name"""
    client = getClient()
    # simple commands for listing container by name
    return [container.name for container in client.containers.list()]


def buildIpImage():
    """Builds a container image based on alpine containing iproute2."""
    f = open("Iproute2.Dockerfile", "rb")
    client = getClient()
    image = client.images.build(fileobj=f, tag="js-iproute2")
    return image
    
def createIpContainer(containerId=""):
    # tmp hard coded id
    containerId = ls()[0] 

    client = getClient()

    image = buildIpImage()

    if image:
        return client.containers.run(
            image[0].id,
            "sleep 30 && echo hello world",
            auto_remove=False, #True,
            cap_add="NET_ADMIN", #Required for traffic control to modify networking.
            detach=True,
            network_mode="container:"+containerId #re-use network stack of the container under attack.
        )
