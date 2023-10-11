import os
import time

import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import (
    Base,
    Car
)

from config import logging


class AutoRiaParser:
    def __init__(self, start_url, database_url):
        self.start_url = start_url
        self.Car = Car
        self.database_url = database_url

        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)

        self.Session = sessionmaker(bind=self.engine)
        self.active_ads: set = set()

    def parse_all_active_ads(self):
        response = requests.get(self.start_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        ads_counter = int(soup.find('span', class_='page-item dhide text-c').text.split('/')[1].replace(' ', ''))
        for i in range(1, ads_counter + 1):
            response = requests.get(self.start_url + str(i))
            car_listings = soup.find_all('section', class_='ticket-item')
            for car_listing in car_listings:
                url = car_listing.find('a', class_='m-link-ticket')['href']
                self.active_ads.add(url)
        logging.info('The data about ads is successfully received')

    def get_all_cars_form_db(self):
        # SQLAlchemy session initialization
        session = self.Session()

        # Retrieve all records from the cars table
        cars = session.query(Car).all()

        # Closing the SQLAlchemy session
        session.close()

        return cars

    @staticmethod
    def get_phone_number(soup: BeautifulSoup):
        """
            Get a phone number associated with a car listing from Auto.Ria.

            Returns:
                str: The formatted phone number in the format +38XXXXXXXXXX.
        """

        auto_id = soup.find('body').get('data-auto-id')
        script = soup.find('script', class_=lambda x: x and "js-user-secure-" in x)
        data_expires = script['data-expires']
        data_hash = script['data-hash']

        url = f'https://auto.ria.com/users/phones/{auto_id}?hash={data_hash}&expires={data_expires}'
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            phone = data.get('formattedPhoneNumber')
            if not phone:
                raise ValueError('Phone number not found in the response.')
            phone = phone.replace("(", "").replace(")", "").replace(" ", "")
            return '+38' + phone

        except requests.exceptions.RequestException as e:
            raise requests.exceptions.RequestException(f'Error with HTTP request: {str(e)}')
        except ValueError as e:
            raise ValueError(f'Error with JSON response: {str(e)}')

    def parse_and_save(self):
        # SQLAlchemy session initialization
        session = self.Session()

        # Sending HTTP request and parsing the page
        for car_url in self.active_ads:
            # Sending a GET request to the page
            response = requests.get(car_url)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                # Retrieve the title
                title = str(soup.find('h1', class_='head').text.strip())

                # Retrieve the phone number
                phone_number = self.get_phone_number(soup)

                # Retrieve the price
                price_element = soup.find('span', class_='price_value').text.strip()
                price_usd = float(price_element.replace(' ', '').replace('$', ''))

                # Extract mileage
                mileage_element = soup.find('div', class_='base-information bold')
                odometer = float(mileage_element.find('span').text.strip()) * 1000

                # Retrieve the number of images
                images_count_element = soup.find('span', class_='count')
                images_count = int(images_count_element.find('span', class_='mhide').text.split(' ')[1])

                # Extract URL image
                image_element = soup.find('div', class_='photo-620x465 loaded')
                if image_element:
                    image_url = str(image_element.picture.source['srcset'])
                else:
                    image_url = 'Not found'

                # Extract username
                username_element = soup.select_one('.seller_info_name, .seller_info_name.bold')
                if username_element:
                    username = username_element.get_text(strip=True)
                else:
                    username = 'Not found'

                # extract the license plate number
                try:
                    car_number = soup.find('div', class_='t-check').find('span', class_='state-num').text.split(' ')[
                                 0:3]
                    car_number = ''.join(i for i in car_number)
                except AttributeError:
                    car_number = 'Hidden'

                # retrieve car license plate number
                try:
                    car_vin = soup.find(class_=['label-vin', 'vin-code']).text
                    car_vin = car_vin
                except AttributeError:
                    car_vin = 'Hidden'

                new_car = Car(link=str(car_url),
                              title=title,
                              price_usd=price_usd,
                              odometer=odometer,
                              username=username,
                              phone_number=phone_number,
                              image_url=image_url,
                              images_count=images_count,
                              car_number=car_number,
                              car_vin=car_vin)
                session.add(new_car)

            else:
                raise Exception(f'Error {response.status_code}')

        session.commit()

        # Close the SQLAlchemy session.
        session.close()
        logging.info(f'The data about ads is successfully received and added to db!')

    def run(self):
        logging.info('Start parse info')

        self.parse_all_active_ads()
        self.parse_and_save()

    def dump(self, dump_directory):
        logging.info('Start dump db')

        # Create a SQLAlchemy session
        session = self.Session()

        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)

        try:
            # Create a database dump
            timestamp = time.strftime("%Y%m%d%H%M%S")
            dump_filename = os.path.join(dump_directory, f'db_backup_{timestamp}.sql')
            dump_command = f'pg_dump {self.database_url} > {dump_filename}'
            os.system(dump_command)

            logging.info(f'Created database dump in {dump_filename}')
        except Exception as e:
            raise Exception(f'An error occurred while creating the dump: {str(e)}')
        finally:
            # Close the SQLAlchemy session.
            session.close()
