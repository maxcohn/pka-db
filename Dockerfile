FROM python:3

# Copy over project files
COPY pka-db/ /app/pka-db/
COPY tools/ /app/tools/
COPY requirements.txt /app/requirements.txt
COPY main.db /app/main.db
COPY .env /app/.env

WORKDIR /app/

# Install server and dependencies
RUN pip3 install gunicorn
RUN pip3 install -r requirements.txt

# Install sqlite3
RUN apt update
RUN apt install sqlite3

# Run the server with 4 worker threads on port 8001
CMD gunicorn -w 4 -b 0.0.0.0:8001 "pka-db:app"
