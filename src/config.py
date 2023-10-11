import os

from dotenv import load_dotenv

import logging

logging.basicConfig(level=logging.INFO)


load_dotenv()

DB_NAME = os.getenv("POSTGRES_DB")
DB_USERNAME = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_ENCODING = os.getenv("POSTGRES_ENCODING")


DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}?{POSTGRES_ENCODING}"


START_URL = 'https://auto.ria.com/uk/car/used/?page='
DUMP_DIRECTORY = "/parser_autoria/dumps"
