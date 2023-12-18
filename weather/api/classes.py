import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import requests
from geopy.geocoders import Nominatim
from pprint import pprint
import meteostat
from datetime import datetime, timedelta

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
        self.weather = Weather(self.lat, self.lon)
    def name(self):
        try:
            location = self.geolocator.reverse(f'{self.lat}, {self.lon}',zoom=10, language="en").raw['address']
            if 'city' in location:
                return location['city']
        except:
            return 'Unknown'
        '''
            Returns an Object of Weather
        '''


class Weather:
    
    def __init__(self, lat, lon, date=None):
        self.lat = lat
        self.lon = lon
        
        if date == None:
            self.date = datetime.now()
        else:
            self.date = date

        start = self.date - timedelta(days=1)
        self.point = meteostat.Point(self.lat, self.lon)
        self.data = meteostat.Daily(self.point, start, self.date)
        self.data = self.data.fetch()
        self.data.fillna(0)

    def get_average_temperature(self):
        average_temperature = self.data.loc[f'{self.date.strftime('%Y-%m-%d')}']['tavg']
        return average_temperature

    def get_minimum_temperature(self):
        minimum_temperature = self.data.loc[f'{self.date.strftime('%Y-%m-%d')}']['tmin']
        return minimum_temperature
    
    def get_maximum_temperature(self):
        maximum_temperature = self.data.loc[f'{self.date.strftime('%Y-%m-%d')}']['tmax']
        return maximum_temperature

    
    def is_rainy(self):
        precepitation = self.data.loc[f'{self.date.strftime('%Y-%m-%d')}']['prcp']
        if precepitation > 2.5:
            return 1
        elif precepitation > 0 and precepitation < 2.5:
            return 2
        else:
            return 0

    
    def is_snowy(self): 
        snow = self.data.loc[f'{self.date.strftime('%Y-%m-%d')}']['snow']
        if snow > 25.4:
            return 1
        elif snow > 0 and snow < 25.4:
            return 2
        else:
            return 0
        return snow
    
    def get_week(self):
        temp = meteostat.Daily(self.point, self.date - timedelta(days=7), self.date)
        temp = temp.fetch()
        temp = temp.fillna(0)
        return temp

    def get_month(self):
        temp = meteostat.Daily(self.point, self.date - timedelta(days=31), self.date)
        temp = temp.fetch()
        temp = temp.fillna(0)
        return temp

    def get_custom_date(self, start, end):
        temp = meteostat.Daily(self.point, self.start, self.end)
        temp = temp.fetch()
        temp = temp.fillna(0)
