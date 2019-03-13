import docker
import os

# Creat docker client
docker_client = docker.from_env()

def getIpFromContainer(container):
	return container.attrs['NetworkSettings']['IPAddress']

def main():
	print("Hello world")
	if not 'RORC_TEST' in os.environ:
		print("Missing required environment variable \"RORC_TEST\"")
		exit(1)
	else:
		container_name = os.environ['RORC_TEST']
		print(container_name)
		print(docker_client.containers.list())
		container = docker_client.containers.get(container_name)
		print(container.name, container.image)

		# Container ip, to be used to filter out network traffic when we launch the networking sidecar container.
		container_ip = getIpFromContainer(container)
		print(container_ip) #
		#print(dir(container.attrs))

# Launches the monitoring sidecars for the docker container.
def startMonitoring(container_name):
	#1. Launch network monitoring utilizing the same networking namespace/stack.
	docker_client.containers.run(
		'jsimo2/royalnetm',
		detach=True,
		network_mode="container:"+container_name)

	#2. Launch syscall monitoring utilizing the same process namespace.
	#docker_client.containers.run(
	#	'jsimo2/royalsysm',
	#	detach=True,
	#	pid_mode="container:"+container_name)

	#3. Maybe (depending on push or pull model) connect monitoring network to container. 

	#4. Verify monitoring, maybe send something on the open port? :hm:

	#5. Report ready...

	pass

if __name__ == '__main__':
    main()
