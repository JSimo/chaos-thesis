FROM alpine

# Required for traffic control
RUN apk --no-cache add iproute2
RUN ln -s /usr/lib/tc /lib/tc

CMD ["/bin/sh"]
