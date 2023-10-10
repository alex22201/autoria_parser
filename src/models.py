import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, DateTime, Float, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
ENCODING = os.getenv("PGCLIENTENCODING")

DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@database:5432/{DB_NAME}?client_encoding={ENCODING}"


class Car(Base):
    __tablename__ = 'cars'

    id: int = Column(Integer, primary_key=True)

    link: str = Column(String)
    title: str = Column(String)
    price_usd: float = Column(Float)
    odometer: float = Column(Float)
    username: str = Column(String)
    phone_number: str = Column(String)
    image_url: str = Column(String)
    images_count: int = Column(Integer)
    car_number: str = Column(String)
    car_vin: str = Column(String)
    datetime_found: datetime = Column(DateTime, default=func.now())

    def __init__(self, link, title, price_usd, odometer, username, phone_number,
                 image_url, images_count, car_number, car_vin):

        self.link = link
        self.title = title
        self.price_usd = price_usd
        self.odometer = odometer
        self.username = username
        self.phone_number = phone_number
        self.image_url = image_url
        self.images_count = images_count
        self.car_number = car_number
        self.car_vin = car_vin

    def __str__(self):
        return f"{self.username}/{self.link} /{self.title}/{self.price_usd}/" \
               f"{self.odometer}/{self.phone_number}/{self.car_number}/{self.car_vin}"



