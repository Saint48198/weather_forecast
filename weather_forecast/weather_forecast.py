__author__ = 'sdaniels'

import urllib.request
import urllib.parse
import simplejson as json
import datetime

from geopy.geocoders import Nominatim

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

    def __init__(self, location):
        if location:
            self.location = str(location)

            geolocator = Nominatim()
            geo_location = geolocator.geocode(self.location)

            self.location = geo_location.address

            # get longitude and latitude
            self.latitude = geo_location.latitude
            self.longitude = geo_location.longitude

             # build the date list
            self.date_list = WeatherForecast.get_date_list(self)
        else:
            print("Bad or no location provided.")

    def get_date_list(self):
        # build the date list
        start_day = datetime.datetime.today()
        date_list = [start_day + datetime.timedelta(days=x) for x in range(0, 5)]

        return date_list


    def get_weather_forecast(self):
        try:
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
                WeatherForecast.output_to_html(self, weather)
        except Exception as e:
            print(e)


    def print_to_console(self, forecast):
        print(self.location + ' (latitude: ' + str(self.latitude) + ' longitude: ' + str(self.longitude) + ')\n')

        array_index = 0

        for day in forecast:
            current_date = str(self.date_list[array_index]).split(' ')[0].split('-')

            print(WeatherForecast.WEEK[self.date_list[array_index].weekday()] + ' - '
                  + WeatherForecast.MONTH[int(current_date[1]) - 1] + ' ' + str(current_date[2]) + ', '
                  + str(current_date[0]))
            print(day['weather'][0]['description'])
            print('High: ' + str(day['temp']['max']) + ' Low: ' + str(day['temp']['min']))
            print('--------------------------------------------------')

            array_index += 1

    def output_to_html (self, forecast):

        array_index = 0

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
                html, body, main, #map-canvas {
                    height: 100%;
                    margin: 0px;
                    padding: 0px
                }
                .navbar-header {
                    color: #fff;
                    padding-top: 12px;
                }
                .container-forecast {
                    position: absolute;
                    bottom: 0;
                    right: 0;
                    left: 0;
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
        """ + self.location + " (latitude: " + str(self.latitude) + " longitude: " + str(self.longitude) + ")" + """
                </div>
            </div>
        </header>
        <main>
            <div id="map-canvas"></div>
            <div class="container-forecast">
                <ol>
        """

        # build the forecast html
        for day in forecast:
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

        # end of the html content
        html_str += """
                     </ol>
                </div>
            </main>
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp"></script>
            <script>
                var map;
                function initialize() {
                    var myLatlng = new google.maps.LatLng(""" + str(self.latitude) + ", " +  str(self.longitude) + """ );
                    var mapOptions = {
                        zoom: 11,
                        scrollwheel: false,
                        navigationControl: false,
                        mapTypeControl: false,
                        scaleControl: false,
                        draggable: false,
                        center: myLatlng
                    };
                    var map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
                    var marker = new google.maps.Marker({
                        position: myLatlng,
                        map: map,
                        title: '""" + self.location + """'
                    });
                }

                google.maps.event.addDomListener(window, 'load', initialize);

            </script>
        </body>
        </html>
        """

        # creating the file and writing its content
        html_file = open('forecast.html', 'w')
        html_file.write(html_str)
        html_file.close()



#testing
#location0 = WeatherForecast("Springfield")
#location0.get_weather_forecast()
#print(location0.longitude)
#WeatherForecast("Ann Arbor, MI")
#WeatherForecast("London") # still fails
#WeatherForecast()