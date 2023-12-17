from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .classes import *


def today(request, lat, lon):
    # lat between -90 & 90
    # lon between -180 & 180
    if lat < -90 or lat > 90:
        return HttpResponseBadRequest("Invalid Latitude Value, Should Be Within -90 and 90.")
    if lon < -180 or lon > 180:
        return HttpResponseBadRequest("Invalid Latitude Value, Should Be Within -180 and 180.")
    
    city = Location(lat, lon)
    weather = Weather(lat, lon)
    response = [city.city(),]
    print(weather.get_current_tempreture())
    response.append(weather.get_current_weather_code())
    return HttpResponse(response)
