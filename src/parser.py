import os
import time

import requests
from bs4 import BeautifulSoup

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Car, Base


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
        soup = BeautifulSoup(response.content, "html.parser")

        ads_counter = int(soup.find('span', class_='page-item dhide text-c').text.split('/')[1].replace(' ', ''))
        for i in range(1, ads_counter + 1):
            response = requests.get(self.start_url + str(i))
            car_listings = soup.find_all("section", class_="ticket-item")
            for car_listing in car_listings:
                url = car_listing.find('a', class_='m-link-ticket')['href']
                self.active_ads.add(url)
        print('The data about ads is successfully received')

    def get_cars(self):
        # SQLAlchemy session initialization
        session = self.Session()

        # Retrieve all records from the cars table
        cars = session.query(Car).all()

        # Closing the SQLAlchemy session
        session.close()

        return cars

    def parse_and_save(self):
        # SQLAlchemy session initialization
        session = self.Session()

        # Sending HTTP request and parsing the page
        for car_url in self.active_ads:
            # Sending a GET request to the page
            response = requests.get(car_url)

            # Check if the request was successful
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # Retrieve the title
                title = str(soup.find('h1', class_='head').text.strip())

                # Retrieve the price
                price_element = soup.find('span', class_='price_value').text.strip()
                price_usd = float(price_element.replace(' ', '').replace('$', ''))

                # Extract mileage
                mileage_element = soup.find('div', class_='base-information bold')
                odometer = float(mileage_element.find('span').text.strip()) * 1000

                # Extract username
                username_element = soup.find(class_=['seller_info_name bold', 'seller_info_name'])
                username = str(username_element.text.strip())

                # Retrieve the phone number
                #TODO:
                # - from 3800XXXXXX format to normal
                phone_element = soup.find('span', class_='mhide')
                phone_number = str(phone_element.text.strip())

                # Extract URL image
                image_element = soup.find('div', class_='gallery-order carousel')
                image_url = str(image_element.picture.source['srcset'])

                # Retrieve the number of images
                images_count_element = soup.find('span', class_='count')
                images_count = int(images_count_element.find('span', class_='mhide').text.split(' ')[1])

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
                raise Exception(f"Error {response.status_code}")

        session.commit()

        # Close the SQLAlchemy session.
        session.close()
        print(f'The data about ads is successfully received and added to db!')

    def run(self):
        print('start run')

        self.parse_all_active_ads()
        self.parse_and_save()

    def dump(self, dump_directory):
        # Create a SQLAlchemy session
        session = self.Session()

        if not os.path.exists(dump_directory):
            os.makedirs(dump_directory)

        try:
            # Create a database dump
            timestamp = time.strftime("%Y%m%d%H%M%S")
            dump_filename = os.path.join(dump_directory, f"db_backup_{timestamp}.sql")
            dump_command = f"pg_dump {self.database_url} > {dump_filename}"
            os.system(dump_command)

            print(f"Created database dump in {dump_filename}")
        except Exception as e:
            raise Exception(f"An error occurred while creating the dump: {str(e)}")
        finally:
            # Close the SQLAlchemy session.
            session.close()
