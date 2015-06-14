__author__ = 'sdaniels'

import datetime
import os
import simplejson as json
import urllib.parse
import urllib.request
import webbrowser

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

class WeatherForecast:

    WEEK = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',  'Friday', 'Saturday', 'Sunday']
    MONTH = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JULY', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
    ICONS = {
        '01d': 'wi-day-sunny',
        '02d': 'wi-cloudy',
        '03d': 'wi-day-sunny-overcast',
        '04d': 'wi-day-cloudy-windy',
        '09d': 'wi-showers',
        '10d': 'wi-rain',
        '11d': 'wi-thunderstorm',
        '13d': 'wi-snow',
        '50d': 'wi-day-fog'
    }
    UNKNOWN_ICON = 'wi-alien'
    HTML = 'forecast.html'

    def __init__(self, location=''):
        if location:
            user_input = str(location)
            user_input_array = user_input.split('|')

            self.locations = list()

            # exception handler for the geolocation call, which can be temperamental every once in a while
            try:
                geolocator = Nominatim()

                for input_value in user_input_array:

                    geo_location = geolocator.geocode(input_value, timeout=10)

                    self.locations.append({
                        'input': input_value,
                        'geo_location': geo_location,
                        'display_location': geo_location.address,
                        'latitude': geo_location.latitude,
                        'longitude': geo_location.longitude
                    })

                 # build the date list
                self.date_list = WeatherForecast.get_date_list(self)
            except GeocoderTimedOut as e:
                print("Error: geocode failed on input %s with timeout error" % user_input)
        else:
            print("Bad or no location provided.")

    def get_date_list(self):
        # build the date list
        start_day = datetime.datetime.today()
        date_list = [start_day + datetime.timedelta(days=x) for x in range(0, 5)]

        return date_list


    def get_weather_forecast(self):
        try:

            for location in self.locations:
                # create the api url
                # using longitude and latitude conversing instead of user input name to simplify param encoding
                api = 'http://api.openweathermap.org/data/2.5/forecast/daily?type=like&units=imperial&cnt=5&lat=' \
                      + str(location['latitude']) + '&lon=' + str(location['longitude'])

                # make the api call
                response = urllib.request.urlopen(api)
                response_data = response.read()
                parse_json = json.loads(response_data)

                # set location weather data
                location['forecast_data'] = parse_json['list']


        except Exception as e:
            print(e)


    def print_to_console(self):

        for location in self.locations:

            print(location['display_location'] + ' (latitude: ' + str(location['latitude']) + ' longitude: ' + str(location['longitude']) + ')\n')

            array_index = 0

            for day in location['forecast_data']:
                current_date = str(self.date_list[array_index]).split(' ')[0].split('-')

                print(WeatherForecast.WEEK[self.date_list[array_index].weekday()] + ' - '
                      + WeatherForecast.MONTH[int(current_date[1]) - 1] + ' ' + str(current_date[2]) + ', '
                      + str(current_date[0]))
                print(day['weather'][0]['description'])
                print('High: ' + str(day['temp']['max']) + ' Low: ' + str(day['temp']['min']))
                print('--------------------------------------------------')

                array_index += 1

            print('--------------------------------------------------\n\n')


    def output_to_html(self):

        # remove the old html file, if there is one
        if os.path.isfile(self.HTML):
            os.remove(self.HTML)

        # create the top html file content
        html_str = """
        <!DOCTYPE html>
        <html>
            <head lang="en">
            <meta charset="UTF-8">
            <title>Weather Forecast</title>
            <!-- Latest compiled and minified Bootstrap CSS -->
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
            <link rel="stylesheet" href="../bower_components/weather-icons/css/weather-icons.min.css">
            <style>
                html, body, main {
                    height: 100%;
                    margin: 0px;
                    padding: 0px
                }
                .map {
                    width: 100%;
                    height: 150px;
                }
                .navbar-header {
                    color: #fff;
                    padding-top: 12px;
                }
                .container-forecast {
                    width: 100%;
                    background: #fff;
                }
                .container-forecast ol {
                    list-style: none;
                    width: 80%;
                    margin: 0 auto;
                }
                .container-forecast li {
                    float: left;
                    width: 20%;
                    color: #666;
                    padding: 15px 0 10px;
                    text-align: center;
                }
                .container-forecast li > div {
                    padding-top: 5px;
                }
                .container-forecast i {
                    font-size: 275%;
                }
            </style>
        </head>
        <body>
            <header class="navbar navbar-inverse navbar-fixed-top">
                <div class="container">
                    <div class="navbar-header">
                    Weather Forecast
                    </div>
                </div>
            </div>
        </header>
        <main>
        """

        # generating each of the locations'  html
        location_index = 0
        for location in self.locations:
            array_index = 0
            html_str += """
                <section>
                    <h1>""" + location['display_location'] + " (latitude: " + str(self.locations[0]['latitude']) + " longitude: " + str(self.locations[0]['longitude']) + ")" + """</h1>
                     <div id="map-canvas""" + str(location_index) + """" class="map"></div>
                     <div class="container-forecast">
                        <ol>"""

            # build the forecast html
            #print(location)
            for day in location['forecast_data']:
                current_date = str(self.date_list[array_index]).split(' ')[0].split('-')
                icon = self.ICONS.get(day['weather'][0]['icon'], self.UNKNOWN_ICON)

                html_str += '<li>' + \
                            '<i class="wi ' + icon + '" title="' + day['weather'][0]['description'] + '"></i>' + \
                            '<div>' + WeatherForecast.WEEK[self.date_list[array_index].weekday()] + \
                            ' - ' + WeatherForecast.MONTH[int(current_date[1]) - 1] + \
                            ' ' + str(current_date[2]) + ', ' + str(current_date[0]) + '<br>' + \
                            'High: ' + str(day['temp']['max']) + '&deg; Low: ' + str(day['temp']['min']) + '&deg;</div>' + \
                            '</li>\n'

                array_index += 1

                location_index += 1
            # end of the location section
            html_str += """
                             </ol>
                        </div>
                    </section>"""

        # generating the js for the maps
        html_str += """</main>
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
            <script>
                var map,
                    myLatlng,
                    mapOptions,
                    marker;
                function initialize() { """

        location_index = 0
        for location in self. locations:
            html_str += """
                myLatlng = new google.maps.LatLng(""" + str(location['latitude']) + ", " + str(location['longitude']) + """ );
                mapOptions = {
                    zoom: 11,
                    scrollwheel: false,
                    navigationControl: false,
                    mapTypeControl: false,
                    scaleControl: false,
                    draggable: false,
                    center: myLatlng
                };
                map = new google.maps.Map(document.getElementById('map-canvas""" + str(location_index) + """'), mapOptions);
                marker = new google.maps.Marker({
                    position: myLatlng,
                    map: map,
                    title: '""" + location['display_location'] + """'
                });"""
            location_index += 1

        #end of the js and the html document
        html_str += """}

                google.maps.event.addDomListener(window, 'load', initialize);

            </script>
        </body>
        </html>
        """

        # creating the file and writing its content
        html_file = open(self.HTML, 'w')
        html_file.write(html_str)
        html_file.close()

        # open the file in the default browser
        self.open_html()

    def open_html(self, file=''):

        if file:
            url = file
        else:
            # used os path because simple file name did nothing
            url = 'file://' + os.path.realpath(self.HTML)

        webbrowser.open_new_tab(url)




#testing
#forecast0 = WeatherForecast("48198")
#forecast0.get_weather_forecast()
#forecast0.print_to_console()
#forecast0.output_to_html()

#location0.output_to_html()
#print(location0.longitude)
#WeatherForecast("Ann Arbor, MI")
#WeatherForecast("London")
#WeatherForecast()