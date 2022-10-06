FROM python:3.8

WORKDIR /app
COPY requirements.txt /app/requirements.txt

RUN apt-get update && pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY . /app
