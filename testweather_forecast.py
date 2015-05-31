__author__ = 'sdaniels'

import unittest
from weather_forecast.weather_forecast import WeatherForecast


class TestWeatherForecast(unittest.TestCase):

    def test_latitude_longitude(self):
        self.location0 = WeatherForecast(48198)
        self.assertEqual(42.259913, self.location0.latitude)
        self.assertEqual(-83.6236289, self.location0.longitude)

        self.location1 = WeatherForecast("Ann Arbor, MI")
        self.assertEqual(42.2681569, self.location1.latitude)
        self.assertEqual(-83.7312291, self.location1.longitude)

        self.location2 = WeatherForecast("London, UK")
        self.assertEqual(51.5073219, self.location2.latitude)
        self.assertEqual(-0.1276474, self.location2.longitude)

    def test_date_list(self):
        self.location0 = WeatherForecast(48198)
        days = self.location0.date_list
        self.assertEqual(5, len(days))