import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from geopy.geocoders import Nominatim
from pprint import pprint


class FloatUrlParameterConverter:
    regex = '-?[0-9]+\.?[0-9]+'

    def to_python(self, value):
        return float(value)

    def to_url(self, value):
        return str(value)

class Location:
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        self.geolocator = Nominatim(user_agent="weather-logger")
    def city(self):
        location = self.geolocator.reverse(f'{self.lat}, {self.lon}',zoom=10, language="en").raw['address']
        if 'city' in location:
            return location['city']


class Weather:
    
    def __init__(self, lat, lon):
        self.url = 'https://api.open-meteo.com/v1/forecast'
        self.lat = lat
        self.lon = lon
        self.params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'hourly': 'temperature_2m',
            'daily' : 'temperature_2m_min',
        }
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = retry_session)
        self.handler = self.openmeteo.weather_api(self.url, params=self.params)
        self.handler = self.handler[0]
        self.current_temperature = None
        self.current_precipitation = None


    def get_hourly(self):        
        return self.handler.Hourly().Variables(0).ValuesAsNumpy()

    def get_daily_min(self):
        return self.handler.Daily().Variables(0).ValuesAsNumpy()
    def get_daily_max(self):
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'daily' : 'temperature_2m_max',
        }
        temp = self.openmeteo.weather_api(self.url, params=params)
        return temp[0].Daily().Variables(0).ValuesAsNumpy()

    def get_daily_weather_code(self):
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'daily' : 'weather_code',
        }
        temp = self.openmeteo.weather_api(self.url, params=params)
        return temp[0].Daily().Variables(0).ValuesAsNumpy()
    
    def hourly_precipitation(self):
        self.handler.Hourly().precipitation()

    def get_current_weather_code(self):
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'current' : 'weather_code',
        }
        temp = self.openmeteo.weather_api(self.url, params=params)        
        return temp[0].Current().Variables(0).Value()
    def get_current_tempreture(self):
        params = {
            'latitude': self.lat,
            'longitude': self.lon,
            'current' : 'temperature_2m',
        }
        temp = self.openmeteo.weather_api(self.url, params=params)        
        return temp[0].Current().Variables(0).Value()

        