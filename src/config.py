import os

from dotenv import load_dotenv

import logging


load_dotenv()

# Logging settings
LOG_MODE = os.getenv('LOG_MODE')

log_level_mapping = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}
logging.basicConfig(level=log_level_mapping.get(LOG_MODE, logging.INFO))

# DB settings
DB_NAME = os.getenv('POSTGRES_DB')
DB_USERNAME = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')


DATABASE_URL = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{DB_NAME}'

# Dumps settings
ROOT_DIR = os.getenv('ROOT_DIR')
DUMP_DIRECTORY = f'{ROOT_DIR}/dumps'


START_URL = 'https://auto.ria.com/uk/car/used/?page='

