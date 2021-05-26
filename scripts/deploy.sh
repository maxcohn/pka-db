#!/bin/sh -e
#
# Deploy to the server

#TODO: param or stdin?
#TODO: error checking
ssh_login="$1"
image_name="pka-db:latest"
healthcheck_url="https://pka-db.com/"

# build the docker image
echo "Building new docker image as: $image_name"
docker build -t "$image_name" .

# send it to the server
echo "Sending it to the server"
docker save "$image_name" | gzip | ssh "$ssh_login" 'gunzip | docker load'

echo 'Logging into server to restart docker container'

# on the server, restart the docker service
ssh "$ssh_login" 'cd pka-db && docker-compose down && docker-compose up -d'

echo 'Waiting 10 seconds before healthcheck'
sleep 10

echo 'Performing health check'
curl -f -IL "$healthcheck_url" && echo "Healthcheck successful"
