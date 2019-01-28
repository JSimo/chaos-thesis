#!/usr/bin/env bash

# ------ Cleanup -------
# Cleanup any old instances of memcached.
echo "Removing old memcaches instances."
docker container rm --force $(docker container ls --filter name=memcache -q)

echo "Finished cleanup"
# Cleanup done

# Create memcache containers and run tests
echo "Deploying two instances of memcache"
docker run -p 11211:11211 -d --name memcached1 memcached:1.5.5
docker run -p 11212:11211 -d --name memcached2 memcached:1.5.5


#echo Hello World!

