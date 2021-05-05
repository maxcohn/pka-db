FROM python:3.8-alpine

# Copy over project files
COPY pka-db/ /app/pka-db/
COPY tools/ /app/tools/
COPY requirements.txt /app/requirements.txt

#COPY main.db /app/main.db
#COPY .env /app/.env

WORKDIR /app/

# Install server and dependencies
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

# shouldn't be necessary since we're mounting the DB now
#RUN apk update && apk add sqlite

# Run the server with 4 worker threads on port 8001
CMD gunicorn -w 4 -b 0.0.0.0:8001 "pka-db:app"
