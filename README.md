# PKA DB

https://pka-db.com

A free and open source website database for Painkiller Already.

## Why?

PKA means a lot to me. I've been listening since late 2011. The show has had a
huge impact on my life and provided me literally thousands of hours of entertainment.

I figured this would be a good introudction to independent web development that
would be used than more than just a handful of friends.

## Goals

## TODO how to suggest

## TODO Getting the data#TODO how to download backup databases


## Running

Use the `run.sh` script to run the development server.

## Deploying

Run `docker build` in the current directory to build the Docker image and run it
to have an active server. By defauly, the server runs on port 8001, so I'd recommend
using the following `docker run`:

```sh
docker run -d -p 8001:8001 -m 200m <image name>
```