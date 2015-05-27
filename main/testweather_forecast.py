__author__ = 'sdaniels'

import unittest
from weather_forecast import WeatherForecast


class TestWeatherForecast(unittest.TestCase):

    def setup(self):
        self.location0 = WeatherForecast(48198)
        self.location1 = WeatherForecast("Ann Arbor, MI")
        self.location2 = WeatherForecast("London")
        self.location3 = WeatherForecast()