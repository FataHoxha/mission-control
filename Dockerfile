# ------------------------------------------------------------- #
# Docker for Api Web App                                        #
# ------------------------------------------------------------- #

# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN mkdir /app/
WORKDIR /app/

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./src/ /app/

ENV FLASK_APP=src/app.py
CMD flask run -h 0.0.0 -p 5000