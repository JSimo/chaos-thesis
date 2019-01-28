FROM alpine:latest
RUN apk add --update htop && rm -rf /var/cache/apk/*
COPY htoprc /root/.config/htop/htoprc
CMD ["htop"]
