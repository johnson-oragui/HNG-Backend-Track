#!/usr/bin/env python3
'''
request module for making api call
'''
from os import getenv
from dotenv import load_dotenv
import requests
import geocoder


# Parse a .env file and then load all the variables
# found as environment variables.
load_dotenv()

# retrieve api_key from env file
API_KEY = getenv('API_KEY')


def user_locate(user_ip) -> tuple:
    '''
    Retrieves the location and weather from a given ip address

    Args:
        user_ip (str): The IP address of the client

    Return:
        tuple:
            city: City location of the client or None
            country: Country location of the Client or None
            temperature: Temperature of the Client's City or None

    '''
    try:
        # get the ip information
        geo = geocoder.ipinfo(user_ip)

        # retrieve the latitude and longitude of the ip address
        location = geo.latlng

        # check if location was retrieved
        if location:
            # separate the latitude and longitude
            lat, lng = location

            # OpenWeather API Call

            # api endpoint for retrieving weather information
            URL = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={API_KEY}&units=metric'

            # send get request to retrieve weather information
            response = requests.get(URL)

            # check if response staus code is ok
            if response.status_code == 200:
                # parse the json encoded content
                data = response.json()

                # retrieve the temperature from the data
                temperature = data.get('main').get('temp')
                # retrieve the country from the data
                country = data.get('sys').get('country')
                # retrieve the city from the data
                city = data.get('name')

                # return city, country, and temperature
                return city, country, temperature
            # if status code is not 200
            else:
                # print to console for debugging purpose
                print('Something went wrong: ', response.status_code)
                # return a tuple of None values
                return None, None, None
    # catch any exception that might occur
    except Exception as exc:
        # print to console for debugging purpose
        print(f'An error occured: {exc}')
        # return a tuple of None values
        return None, None, None
    print('invalid or no ip: ', location, user_ip)
    # if the location was not found or an invalid ip was provided
    # return a tuple of None values
    return None, None, None

if __name__ == '__main__':
    city, country, temperature = user_locate('172.29.148.228')
    print(f'city: {city},\ncountry: {country}\ntemp: {temperature}')
