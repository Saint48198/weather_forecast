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