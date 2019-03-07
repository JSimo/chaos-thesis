
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

## Strace/ptrace
`docker run --pid=container:hello_world --cap-add sys_ptrace -it ubuntu`
`ps -aux` //List running processes.
`strace -p <pid>` //Attach to process and print syscalls.

Realised strace supports fault injection in syscalls! Although it will do it everytime, no fun random or similar.
`strace -e fault=open -p <pid>`
`strace -e inject=open:error=ENOENT -p 6` //Results in 404 from nginx.
`strace -e inject=open:error=EACCES -p 6` //Permission error => 403.
`strace -e inject=open:error=ENOENT:when=1+2 -p 6` //404 every other request.

//Not needed
python library for ptrace? :hmmm:
https://python-ptrace.readthedocs.io/en/latest/usage.html#ptraceprocess


