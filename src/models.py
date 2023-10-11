from datetime import datetime
from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
    Float,
    func
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


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

    def __repr__(self):
        return f"Car({self.title}/{self.price_usd}/{self.link}\n" \
               f"{self.username}/{self.odometer}/{self.phone_number}/{self.car_number}/{self.car_vin})"



