
# Doing network emulation of issues on docker is quite easy as long as you run the containers on linux. 
This is easy as linux has the command traffic control with network emulation capablilites. 
Essentially you create another container (having iproute2 installed) and give it the capability "NET_ADMIN"
and the same network stack as the container under test.


1. `docker run --network=container:3460fd797b2d --cap-add="NET_ADMIN" -it se.jsimo.alpine.iproute2`
2. `tc qdisc add dev eth0 root netem delay 1000ms`

## Cleanup
`tc qdisc del dev eth0 root`


## Future plan
Add ability to add a delay to a specific container. 
Add ability to add execute something at same time?

## Knowledge
Running a tc command and then quitting the container causes the tc command to still exist.

