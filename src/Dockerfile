# NOTE name need to be Dockerfile
FROM python:3.10


COPY /requirements.txt .


RUN pip install -r requirements.txt

WORKDIR /parser_autoria

#ENV DB_USERNAME=admin
#ENV DB_PASSWORD=123456
#ENV DB_NAME=medium_db
#ENV PGCLIENTENCODING=UTF8

COPY main.py /parser_autoria/
COPY models.py /parser_autoria/
COPY parser.py /parser_autoria/

