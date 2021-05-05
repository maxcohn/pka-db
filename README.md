# PKA DB

https://pka-db.com

A free and open source website database for Painkiller Already.

Monthly backups of the database are hosted on the [`releases`](https://github.com/maxcohn/pka-db/releases)
page of this repo.

### **[If you want to contribute, please refer to the contribution guidelines](CONTRIBUTING.md)**

## Why?

PKA means a lot to me. I've been listening since late 2011. The show has had a
huge impact on my life and provided me literally thousands of hours of entertainment.

I figured this would be a good introudction to independent web development that
would be used than more than just a handful of friends.

## Goals

* Create an interactive archive of Painkiller Already

## Planned Improvements

* Guest images
* Guest bios
* Cleaning up design for guest lists on episodes and searches
* Cleaning up design for episode lists on guests

## Suggesting Additions/Improvements

Create an issue with the idea and I'll get around to it when I have the chance.
If you have implementation ideas, please feel free to put them in the issue as well.
As for whether this is going to be open contribution is up in the air at the moment.

## Database Structure

I don't claim to have any expertise in database design, so this might not be the
greatest DDL you've ever seen, but it has been working well.

Tables:
* `show` - Mapping between id and show name.
* `episodes` - Stores show (`PKA` or `PKN`), episode number, runtime, original
airdate, and YouTube link (if applicable).
* `guests` - Stores name and an id.
* `events` - Stores a show and episode, a description/title of the event, and a
timestamp that the event occurs at.
* `appearances` - Appearance of a guest (show, episode, and their id)
* `pending_events` - Same as events table, except this is where submitted events
go until they are approved by the admin.

## Running (development)

Use the `run.sh` script to run the development server.

## Deploying

The following environment variables can be set (don't worry if using docker):
* DB_PATH

If you want the automatic updates:
* YT_API_KEY
* SENDGRID_API_KEY

Run `docker build` in the current directory to build the Docker image and run it
to have an active server. By defauly, the server runs on port 8001, so I'd recommend
using the following `docker run`:

```sh
docker run -d -p 8001:8001 -v "$PWD/main.db:/data/main.db" -v "$PWD/blacklist.txt:/data/blacklist.txt" -m 200m <image name>
```

The use of `-m 200m` isn't necessary, but I do that to make sure it doesn't eat
up too much ram since I run this next to a few other applications on a cheap VPS.


If you want to use the automatic updates, you need to run the script `get-newest-episode.py`.
There are maby ways to go about automating this, but I chose to use a Cron Job
on the host server that calls:

```sh
docker exec CONTAINER python3 /app/tools/get-newest-episode.py <params>
```

Directory structure (so you know where to put `main.db` and `.env`):
```
pka-db/
    pka-db/
        static/
        templates/
        *.py
    .env
    main.db
    requirements.txt
```