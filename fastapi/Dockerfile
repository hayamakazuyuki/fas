FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# copy requirements.txt to current directory
COPY ./requirements.txt ${PWD}

RUN pip install -r requirements.txt

ENV TZ=Asia/Tokyo

WORKDIR /fastapi
