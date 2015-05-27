__author__ = 'sdaniels'

import urllib.request
import urllib.parse
import simplejson as json
import datetime

from geopy.geocoders import Nominatim

WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday', 'Saturday', 'Sunday']

MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

def get_date_list():
    # build the date list
    start_day = datetime.datetime.today() + datetime.timedelta(days=1)
    date_list = [start_day + datetime.timedelta(days=x) for x in range(0, 5)]

    return date_list


def get_weather_forecast(location, latitude, longitude):
    # create the api url
    # using longitude and latitude conversing instead of user input name to simplify param encoding
    api = 'http://api.openweathermap.org/data/2.5/forecast/daily?type=like&units=imperial&cnt=5&lat=' \
          + str(latitude) + '&lon=' + str(longitude)

    # make the api call
    with urllib.request.urlopen(api) as response:
        response_data = response.read()
        parse_json = json.loads(response_data)
        weather = parse_json['list']

        print_weather_forecast(location, latitude, longitude, weather)


def print_weather_forecast(location, latitude, longitude, forecast):
    print(location + '(latitude: ' + str(latitude) + ' longitude: ' + str(longitude) + ')\n')

    # build the date list
    date_list = get_date_list()
    array_index = 0

    for day in forecast:
        current_date = str(date_list[array_index]).split(' ')[0].split('-')

        print(WEEK[date_list[array_index].weekday()] + ' - ' + MONTH[int(current_date[1]) - 1] + ' ' + str(current_date[2]) + ', ' + str(current_date[0]))
        print(day['weather'][0]['description'])
        print('High: ' + str(day['temp']['max']) + ' Low: ' + str(day['temp']['min']))
        print('--------------------------------------------------')

        array_index += 1


def init():
    location = input('Enter your location (Example: Ann Arbor, MI US or London, UK\n');

    if(location):

        geolocator = Nominatim()
        geo_location = geolocator.geocode(location)

        # get longitude and latitude
        latitude = geo_location.latitude
        longitude = geo_location.longitude


        get_weather_forecast(location, latitude, longitude)



init()