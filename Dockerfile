FROM python:3.7-slim

RUN apt -y update
RUN apt -y upgrade

RUN apt install -y sqlite3 libsqlite3-dev

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install pipenv

COPY ./Pipfile /app/Pipfile
RUN pipenv install --skip-lock --system --dev

COPY . /app
RUN ./manage.py migrate
RUN ./configure.sh

CMD ./manage.py runserver 0.0.0.0:8000