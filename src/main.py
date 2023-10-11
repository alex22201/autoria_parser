import time
import schedule as schedule

from parser import AutoRiaParser
from config import (
    DATABASE_URL,
    DUMP_DIRECTORY,
    START_URL
)


if __name__ == "__main__":
    parser = AutoRiaParser(START_URL, DATABASE_URL)
    schedule.every().day.at("12:00").do(parser.run)
    schedule.every().day.at("00:00").do(parser.dump, DUMP_DIRECTORY)
    # Start scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
