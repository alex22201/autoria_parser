# NOTE name need to be Dockerfile
FROM python:3.10

RUN apt-get update && apt-get install -y postgresql-client-15

COPY /requirements.txt .

RUN pip install -r requirements.txt

WORKDIR ${ROOT_DIR}

COPY *.py ${ROOT_DIR}/
