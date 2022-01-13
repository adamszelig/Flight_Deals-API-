#This file will need to use the DataManager,FlightSearch, FlightData, NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_data import FlightData
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "BUD"

flight_sheet = DataManager()
notification_manager = NotificationManager()
# flight_sheet.write()
# flight_readout = flight_sheet.read()
# print(flight_readout)
flight_readout = [{'city': 'Paris', 'iataCode': 'PAR', 'lowestPrice': 20000, 'id': 2}, {'city': 'Berlin', 'iataCode': 'BER', 'lowestPrice': 10000, 'id': 3}, {'city': 'Tokyo', 'iataCode': 'TYO', 'lowestPrice': 50000, 'id': 4}, {'city': 'Sydney', 'iataCode': 'SYD', 'lowestPrice': 50000, 'id': 5}, {'city': 'New York', 'iataCode': 'NYC', 'lowestPrice': 50000, 'id': 6}]
flight_search = FlightSearch()

tomorrow = datetime.now() + timedelta(days=1)
one_month_from_today = datetime.now() + timedelta(days=60)

for destination in flight_readout:
    city = destination["city"]
    iata = destination["iataCode"]
    low_price = destination["lowestPrice"]
    found_searches = flight_search.search(origin_city_code=ORIGIN_CITY_IATA, destination_city_code=iata, from_time=tomorrow, to_time=one_month_from_today)
    if found_searches is None:
        continue
    if found_searches.price < destination["lowestPrice"]:
        # notification_manager.send_sms(message=f"Low price alert! Only {found_searches.price}HUF to fly from {found_searches.origin_city}-{found_searches.origin_airport} to {found_searches.destination_city}-{found_searches.destination_airport}, from {found_searches.out_date} to {found_searches.return_date}.")
        # print("cheaper")
        users = flight_sheet.get_customer_emails()
        emails = [row["email"] for row in users]
        names = [row["firstName"] for row in users]
        message = f"Low price alert! Only {found_searches.price}HUF to fly from {found_searches.origin_city}-{found_searches.origin_airport} to {found_searches.destination_city}-{found_searches.destination_airport}, from {found_searches.out_date} to {found_searches.return_date}."
        # if flight.stop_overs > 0:
        #     message += f"\nFlight has {flight.stop_overs} stop over, via {flight.via_city}."

        link = f"https://www.google.com/flights?hl=en#flt{found_searches.origin_airport}.{found_searches.destination_airport}.{found_searches.out_date}*{found_searches.destination_airport}.{found_searches.origin_airport}.{found_searches.return_date}"
        #notification_manager.send_emails(emails, message, link)
