FROM python:3.10.6-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV TZ=Europe/Moscow

RUN apt-get -qqy update && apt-get -qqy  install gcc git && pip install poetry && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
WORKDIR /shopbot
COPY poetry.lock pyproject.toml /shopbot/
RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /shopbot
WORKDIR /shopbot
# run entrypoint.sh

