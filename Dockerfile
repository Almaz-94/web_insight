FROM python:3.11-slim

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN apt-get update && apt-get install -y --no-install-recommends make curl \
    && apt-get install nano && apt-get install vim -y  \
    && apt-get clean \
    && pip install --upgrade pip \
    && apt-get install -y ffmpeg

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . .
