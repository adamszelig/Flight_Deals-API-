import requests
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv("./.env")

TOKEN = os.environ.get("TOKEN")
sheet_endpoint = os.environ.get("SHEET_ENDPOINT")


class DataManager:
    def __init__(self):
        self.city = ""
        self.iata = ""
        self.price = ""

    def write(self):
        self.city = input("Where would you like to travel?: ")
        self.iata = input("What is the IATA code?: ")
        self.price = input("What is the price?: ")
        sheet_inputs = {
            "flight": {
                "city": self.city,
                "iataCode": self.iata,
                "lowestPrice": self.price
            }
        }

        sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)

        # # Basic Authentication
        # basic_headers = {
        #     "Authorization": f"Basic {TOKEN}"
        # }
        # sheet_response = requests.post(
        #     sheet_endpoint,
        #     json=sheet_inputs,
        #     headers=basic_headers
        # )

        #print(sheet_response.text)

    def read(self):
        sheet_inputs = {
            "flight": {
                "city": self.city,
                "iataCode": self.iata,
                "lowestPrice": self.price
            }
        }

        sheet_response = requests.get(sheet_endpoint, json=sheet_inputs)
        sheet_data = sheet_response.json()["flights"]
        #print(sheet_response.text)
        #print(sheet_data)
        return sheet_data

    def get_customer_emails(self):
        customers_endpoint = "https://api.sheety.co/1cf212a4ca07141517564d10d0560631/flightPrices/users"
        response = requests.get(customers_endpoint)
        data = response.json()["users"]
        self.customer_data = data
        return data
