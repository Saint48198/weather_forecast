__author__ = 'sdaniels'

import urllib.request
import urllib.parse
import simplejson as json
import datetime

from geopy.geocoders import Nominatim

class WeatherForecast:

    WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday', 'Saturday', 'Sunday']
    MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

    def __init__(self, location):
        if location:
            self.location = str(location)
        else:
            self.location = input('Enter your location (Example: Ann Arbor, MI US or London, UK\n')

        geolocator = Nominatim()
        geo_location = geolocator.geocode(self.location)

        self.location = geo_location.address

        # get longitude and latitude
        self.latitude = geo_location.latitude
        self.longitude = geo_location.longitude

    def get_date_list(self):
        # build the date list
        start_day = datetime.datetime.today() #+ datetime.timedelta(days=1)
        date_list = [start_day + datetime.timedelta(days=x) for x in range(0, 5)]

        return date_list


    def get_weather_forecast(self):
        # create the api url
        # using longitude and latitude conversing instead of user input name to simplify param encoding
        api = 'http://api.openweathermap.org/data/2.5/forecast/daily?type=like&units=imperial&cnt=5&lat=' \
              + str(self.latitude) + '&lon=' + str(self.longitude)
        #print(api)
        # make the api call
        with urllib.request.urlopen(api) as response:
            response_data = response.read()
            parse_json = json.loads(response_data)
            weather = parse_json['list']

            WeatherForecast.print_to_console(self, weather)
            WeatherForecast.print_to_html(self, weather)


    def print_to_console(self, forecast):
        print(self.location + '(latitude: ' + str(self.latitude) + ' longitude: ' + str(self.longitude) + ')\n')

        # build the date list
        date_list = WeatherForecast.get_date_list(self)
        array_index = 0

        for day in forecast:
            current_date = str(date_list[array_index]).split(' ')[0].split('-')

            print(WeatherForecast.WEEK[date_list[array_index].weekday()] + ' - '
                  + WeatherForecast.MONTH[int(current_date[1]) - 1] + ' ' + str(current_date[2]) + ', '
                  + str(current_date[0]))
            print(day['weather'][0]['description'])
            print('High: ' + str(day['temp']['max']) + ' Low: ' + str(day['temp']['min']))
            print('--------------------------------------------------')

            array_index += 1

    def print_to_html (self, forecast):
        # build the date list
        date_list = WeatherForecast.get_date_list(self)
        array_index = 0

        # create the top html file content
        html_str = """
        <!DOCTYPE html>
        <html>
            <head lang="en">
            <meta charset="UTF-8">
            <title>Weather Forecast</title>
        </head>
        <body>
            <header>
        """ + self.location + " (latitude: " + str(self.latitude) + " longitude: " + str(self.longitude) + ")" + """
            </header>
            <main>
                <ol>
        """

        # build the forecast html
        for day in forecast:
            current_date = str(date_list[array_index]).split(' ')[0].split('-')

            html_str += '<li>' + \
                        WeatherForecast.WEEK[date_list[array_index].weekday()] + \
                        ' - ' + WeatherForecast.MONTH[int(current_date[1]) - 1] + \
                        ' ' + str(current_date[2]) + ', ' + str(current_date[0]) + \
                        '<br>' + day['weather'][0]['description'] + '<br>' + \
                        'High: ' + str(day['temp']['max']) + ' Low: ' + str(day['temp']['min']) + \
                        '</li>'

        # end of the html content
        html_str += """
                </ol>
            </main>
        </body>
        </html>
        """

        html_file = open('forecast.html', 'w')
        html_file.write(html_str)
        html_file.close()

#testing
location0 = WeatherForecast("London, GB")
location0.get_weather_forecast()
#print(location0.longitude)
#WeatherForecast("Ann Arbor, MI")
#WeatherForecast("London") # still fails
#WeatherForecast()