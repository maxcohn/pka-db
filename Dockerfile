FROM python:3

COPY pka-db/ /app/pka-db/
COPY requirements.txt /app/requirements.txt
COPY main.db /app/main.db
COPY .env /app/.env

WORKDIR /app/

RUN pip3 install gunicorn

RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:8001 "pka-db:app"
