#/usr/bin/env bash
docker build . -t htop
docker run -it --rm --pid=host htop
