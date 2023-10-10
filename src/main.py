import time
import schedule as schedule

from models import DATABASE_URL
from parser import AutoRiaParser


if __name__ == "__main__":
    START_URL = 'https://auto.ria.com/uk/car/used/?page='
    DUMP_DIRECTORY = "/parser_autoria/dumps"

    parser = AutoRiaParser(START_URL, DATABASE_URL)

    schedule.every().day.at("23:20").do(parser.run)
    schedule.every().day.at("23:24").do(parser.dump, DUMP_DIRECTORY)

    # Start scheduler
    while True:
        schedule.run_pending()

        time.sleep(1)
