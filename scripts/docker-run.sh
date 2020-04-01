#!/bin/sh

# the gunicorn server runs on port 8001

docker run -d -p 8002:8001 --name pka-db --env-file .env pka-db:latest