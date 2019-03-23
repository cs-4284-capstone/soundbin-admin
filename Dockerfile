FROM python:3.7-slim

RUN apt -y update
RUN apt -y upgrade

RUN apt install -y sqlite3 libsqlite3-dev
RUN pip install pipenv

COPY . /app
WORKDIR /app

RUN pipenv install
RUN pipenv run ./manage.py migrate
RUN ./configure.sh

CMD pipenv run ./manage.py runserver 0.0.0.0:8000