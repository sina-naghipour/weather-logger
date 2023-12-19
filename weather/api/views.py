from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseServerError
from .classes import *
import meteostat
from datetime import datetime, timedelta
import re

def today(request, lat, lon):
    # lat between -90 & 90
    # lon between -180 & 180
    if lat < -90 or lat > 90:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -90 and 90.')
    if lon < -180 or lon > 180:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -180 and 180.')
    city = Location(lat, lon)
    weather = city.weather
    return HttpResponse(weather.get_daily_data())

def history(request, lat, lon, start, end):

    # lat between -90 & 90
    # lon between -180 & 180
    if lat < -90 or lat > 90:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -90 and 90.')
    if lon < -180 or lon > 180:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -180 and 180.')
    # check format of start and end which should be xxxx-xx-xx (year-month-day)
    date_regex = r'^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$'
    if not re.match(date_regex, start):
        return HttpResponseBadRequest('The Start Date You\'ve Requested is Not Quite The Right Format')

    if not re.match(date_regex, end):
        return HttpResponseBadRequest('The End Date You\'ve Requested is Not Quite The Right Format')

    city = Location(lat, lon)
    try:
        start = datetime.strptime(start, '%Y-%m-%d')
        end = datetime.strptime(end, '%Y-%m-%d')
    except:
        return HttpResponseBadRequest('Invalid Date.')    
    temp = end - start
    if(temp.days <= 0):
        return HttpResponseBadRequest('Dates are not Valid.')
    weather = city.weather.get_custom_date(start, end)
    if weather.empty:
        return HttpResponse('No Data Available')
    return HttpResponse(weather)

def today_temperature(request, lat, lon):
    # lat between -90 & 90
    # lon between -180 & 180
    if lat < -90 or lat > 90:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -90 and 90.')
    if lon < -180 or lon > 180:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -180 and 180.')
    try:
        city = Location(lat, lon)
        weather = city.weather
    except:
        return HttpResponseServerError('Server Not Responding, Please Try Again.')

    return HttpResponse(weather.get_average_temperature())

def today_current(request, lat, lon):
    # lat between -90 & 90
    # lon between -180 & 180
    if lat < -90 or lat > 90:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -90 and 90.')
    if lon < -180 or lon > 180:
        return HttpResponseBadRequest('Invalid Latitude Value, Should Be Within -180 and 180.')
    try:
        city = Location(lat, lon)
        weather = city.weather
    except:
        return HttpResponseServerError('Server Not Responding, Please Try Again.')

    return HttpResponse(weather.get_current_hour())

