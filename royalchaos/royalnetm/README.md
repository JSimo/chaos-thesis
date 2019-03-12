# README
`docker run --network=container:3460fd797b2d --cap-add="NET_ADMIN" -it <image>`


# The problem.
Attaching to another container network will make it impossible to open ports the other container has already opened to the outside world.
This is a problem as prometheus works on the scrabe model, instead of data being push to prometheus. For prometheus to be able to scrabe the service under test we will have to work around this by letting the container under test attach to prometheus network, so they both can see each other. Now the data should be available in the prometheus for further processing.

# SETUP (kind of)
0. decide on what container you want to monitor.
1. Launch monitoring sidecar container, using the network namespace of that container.
`docker run --network=container:<name> --cap_add="NET_ADMIN" jsimo2/royalnetm`
2. Launch prometheus, configure it to scrape port 12301 on the container you want to monitor.
`docker network connect <network-of-prometheus> <container-to-monitor>`
3. Now look at prometheus to see if the logs are working as they should.

# TODO, simplify this setup.
prometheus automated service discovery: https://prometheus.io/docs/prometheus/latest/configuration/configuration/#%3Cfile_sd_config
important things to think about: networking interface, ip address filters? other concerns?

# Next steps after:
syscall monitoring by sharing the PID namespace. <- This usecase should be easier to export metrics to prometheus as we will then have the network free.

# prometheus queries.
sum(http_request_total) by (uri)
sum(http_request_total) by (uri)

# design thoughts:
master agent:
  -> launches monitoring sidecar (with a correct config to filter on ip etc.)
  -> updates prometheus scraping config that is mouted somewhere accessable. 
  -> adds prometheus server network to the container under test. 
  -> verifies that networked container monitoring metrics have started to be recorded. (This step requires there to be traffic passing to the container, if it is doing nothing, hard to verify, maybe send a invalid request to the port(s) that we scrape from the docker api.)
  -> launch syscall monitoring sidecar (shared pid-namespace)
  -> connect network prometheus network to syscall monitoring sidecar. 
  -> verify that the sidecar is giving us data.
  -> READY for experiments! Now we have reached observability! 
  -> Execute perturbation.
  -> Watch metrics => give conclucsions based on metric.
  