import datetime
from datetime import datetime, timedelta, date
import os
import googlemaps
import twilio
from twilio.rest import Client
import json


with open("practice/apiconfig.json") as f:
     configfile = json.load(f)

def getweekday():
    given_date = date.today()
    given_date = given_date.weekday()
    day ={
        1 : "Monday",
        2: "Tuesday",
        3: "Wendsday",
        4: "Thursday",
        5: "Friday"
    }
    given_date = day[given_date+1]  
    return given_date
        
def get_commute_duration():

    home_address = configfile["home_adress"]
    destination_address = configfile["destination_address"]
        
    google_maps_api_key = configfile["gmaps_api_key"]
    gmaps = googlemaps.Client( key=google_maps_api_key)

    directions = gmaps.directions(home_address,destination_address)
    first_leg = directions[0]['legs'][0]
    duration = first_leg['duration']['text']
    duration = int(duration[:2])
    return duration

def send_text_message(message):
     
    account_sid = configfile["Twilio_sid"]
    auth_token = configfile["Twilio_token"]
    client = Client(account_sid, auth_token)

    message = client.messages.create(
    from_='+18727135299',
    body=str(message),
    to='+18329436724'
    )

def main():
    duration = get_commute_duration()
    now = datetime.now()
    arrival_time = (now + timedelta(minutes=duration)).strftime('%I:%M %p')
    message = (
        f"Good morning Anthony! Happy {getweekday()}.\n\n"
        f"Estimated commute time from home to work at {datetime.now().strftime('%I:%M %p')} : { str(duration) } minutes.\n"
        f"Estimated Arrival time: { str(arrival_time)}.\n"
        f"Have a nice day and give it your best!!!")
    
    print(message)
    send_text_message(message)


if __name__ == "__main__":
        main()