from django.shortcuts import render
from django.views import View
import folium
import requests
import httpx
import asyncio
import numpy as np
import pandas as pd
import random
from folium.plugins import HeatMap

def similar_mark(point):
    rand = random.randint(0,3)
    if rand == 0:
        point[0] -= 0.01
    elif rand == 1:
        point[0] += 0.01

    elif rand == 2:
        point[1] -= 0.01
    elif rand == 3:
        point[1] += 0.01
    return point

async def fetch_current_temperature(point):
    url = f'http://127.0.0.1:8008/api/today/current/{point[0]}/{point[1]}'
    async with httpx.AsyncClient() as client:
        print(point)
        try:
            response = await client.get(url)
        except:
            raise SystemError('Couldn\'t fetch data.')
        result = response.json()
        if 'temp' in result:
            if result['temp'] == {}:
                mark = similar_mark(point)
                return await fetch_current_temperature(mark)
        return response.json()

def random_point(axis, x_axis, y_axis):
    rand = random.randint(0,3)
    x, y = axis
    if rand == 0:
        x = random.uniform(axis[0], random.choice(x_axis))
    if rand == 1:
        x = random.uniform(axis[0], random.choice(x_axis))
    if rand == 2:
        y = random.uniform(axis[1], random.choice(y_axis))
    if rand == 3:
        y = random.uniform(axis[1], random.choice(y_axis))
    axis[0] = x
    axis[1] = y
    return axis


class Map(View):

    async def get(self, request, lat, lon):
        m = folium.Map(location=[lat, lon], zoom_start=10)

        axis = [lat, lon]
        marks = [[axis[0]+0.20, axis[1]-0.20],[axis[0]-0.0130, axis[1]+0.3012], [axis[0]-0.1530, axis[1]-0.0542], [axis[0]-0.0423, axis[1]-0.2860], [axis[0], axis[1]] ]
        x_axis = [mark[0] for mark in marks]
        y_axis = [mark[1] for mark in marks]

        arr = np.array([axis]*500)
        m = folium.Map(axis, zoom_start=10)
        data = []
        for i in range(500):
            if i == 0:
                continue
            arr[i] = random_point(arr[i-1], x_axis, y_axis)
            data.append(arr[i].tolist())

        marks = [[axis[0]+0.20, axis[1]-0.20],[axis[0]-0.0130, axis[1]+0.3012], [axis[0]-0.1530, axis[1]-0.0542], [axis[0]-0.0423, axis[1]-0.2860], [axis[0], axis[1]] ]

        handler = [fetch_current_temperature(mark) for mark in marks]
        results = await asyncio.gather(*handler)

        for mark in marks:
            DF = pd.DataFrame(results)
            temperature = DF.loc[marks.index(mark)]['temp']
            for item in temperature:
                temperature = item[1]

            folium.Marker(mark, popup=temperature).add_to(m)
        temperature = DF.loc[0]['temp']
        for item in temperature:
            temperature = item[1]
        temperature = int(temperature)

        for i in range(499):
            data[i].append(random.uniform(temperature - 1 , temperature + 1))
        if temperature < 8:
            gradient={
                0.6: 'cyan',
                0.8: 'blue',
                1: 'purple'
            }
        if temperature < 20 and temperature > 8:
             gradient={
                0.6: 'green',
                0.8: 'yellow',
                1: 'orange'
            }       
        if temperature > 20:
             gradient={
                0.6: 'yellow',
                0.8: 'orange',
                1: 'red'
            }       
        
        HeatMap(data, min_opacity=0.3, max_val=temperature, radius=20, gradient=gradient).add_to(m)
        map_html = m._repr_html_()
        
        return render(request, 'map/index.html', {'map_html' : map_html})
