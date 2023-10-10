# NOTE name need to be Dockerfile
FROM python:3.10

COPY /requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /parser_autoria

COPY main.py /parser_autoria/
COPY models.py /parser_autoria/
COPY parser.py /parser_autoria/

