import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from flight_data import FlightData

load_dotenv("./.env")

ACC_NAME = os.environ.get("ACC_NAME")
EMAIL = os.environ.get("EMAIL")
PASS = os.environ.get("PASS")
API_KEY = os.environ.get("API_KEY")
AFFIL_ID = os.environ.get("AFFIL_ID")
TEQUILA_ENDPOINT = os.environ.get("TEQUILA_ENDPOINT")

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.

    def search(self, origin_city_code, destination_city_code, from_time, to_time):
        headers = {"apikey": API_KEY}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 2,
            "nights_in_dst_to": 7,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "HUF"
        }

        response = requests.get(
            url=TEQUILA_ENDPOINT,
            headers=headers,
            params=query,
        )


        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            out_airline=data["route"][0]["airline"],
            out_flight=data["route"][0]["flight_no"],
            return_date=data["route"][1]["local_departure"].split("T")[0],
            return_airline = data["route"][1]["airline"],
            return_flight = data["route"][1]["flight_no"]
        )

        print(f"{flight_data.destination_city}: {flight_data.price}HUF {flight_data.out_airline} {flight_data.out_flight}")

        return flight_data
