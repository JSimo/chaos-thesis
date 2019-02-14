import docker

IPROUTE2_IMAGE_TAG = "se.jsimo.alpine.iproute2"

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
    image = client.images.build(
        fileobj=f, 
        tag=IPROUTE2_IMAGE_TAG)
    return image

def filterContainers():
    """Filters out all containers containg the tag "se.jsimo.alpine.iproute2"""
    client = getClient()
    return [c for c in client.containers.list() if IPROUTE2_IMAGE_TAG not in c.image.tags[0]]
    

def execTcCmd(containerId, cmd):
    client = getClient()

    image = buildIpImage()
 
    return client.containers.run(
        image[0].id,
        cmd, # command to execute
        cap_add="NET_ADMIN", #Required for traffic control to modify networking.
        detach=True,
        network_mode="container:"+containerId #re-use network stack of the container under attack
    )

def createIpContainer(containerId=""):
    # The first container not being any weird copies of ourself left running
    containerId = filterContainers()[0].id

    client = getClient()

    image = buildIpImage()

    if image:
        return client.containers.run(
            image[0].id,
            #auto_remove=False, #True,
            cap_add="NET_ADMIN", #Required for traffic control to modify networking.
            detach=True,
            network_mode="container:"+containerId, #re-use network stack of the container under attack.
            #tty=True # Add tty to keep container running? Do we need to keep the container running?
        )


def testExec():
    """test method"""


