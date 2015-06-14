__author__ = 'sdaniels'

import os
import unittest
from weather_forecast.weather_forecast import WeatherForecast


class TestWeatherForecast(unittest.TestCase):

    def test_3rd_party_api_response(self):
        self.forecast0 = WeatherForecast("Springfield")
        self.forecast0.get_weather_forecast()
        self.assertEqual(5, len(self.forecast0.locations[0]['forecast_data']))

        self.forecast1 = WeatherForecast(48198)
        self.forecast1.get_weather_forecast()
        self.assertEqual(5, len(self.forecast1.locations[0]['forecast_data']))

        self.forecast2 = WeatherForecast("Boston, MA")
        self.forecast2.get_weather_forecast()
        self.assertEqual(5, len(self.forecast2.locations[0]['forecast_data']))

    def test_date_list(self):
        self.forecast0 = WeatherForecast(48198)
        days = self.forecast0.date_list
        self.assertEqual(5, len(days))

    def test_html_exists(self):
        self.forecast0 = WeatherForecast(48198)
        self.forecast0.get_weather_forecast()
        self.forecast0.output_to_html()
        self.assertEqual(True, os.path.isfile('weather_forecast/forecast.html'))

    def test_multiple_locations(self):
        self.forecast0 = WeatherForecast("48198|London")
        self.assertEqual(2, len(self.forecast0.locations))

        self.forecast0.get_weather_forecast()
        self.assertEqual(5, len(self.forecast0.locations[0]['forecast_data']))
        self.assertEqual(5, len(self.forecast0.locations[1]['forecast_data']))

    def test_latitude_longitude(self):
        self.forecast0 = WeatherForecast(48198)
        self.assertEqual(42.2598978, self.forecast0.locations[0]['latitude'])
        self.assertEqual(-83.6236275, self.forecast0.locations[0]['longitude'])

        self.forecast1 = WeatherForecast("Ann Arbor, MI")
        self.assertEqual(42.2681569, self.forecast1.locations[0]['latitude'])
        self.assertEqual(-83.7312291, self.forecast1.locations[0]['longitude'])

        self.forecast2 = WeatherForecast("London")
        self.assertEqual(51.5073219, self.forecast2.locations[0]['latitude'])
        self.assertEqual(-0.1276474, self.forecast2.locations[0]['longitude'])


