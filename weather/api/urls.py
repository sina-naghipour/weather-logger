from django.urls import path
from .views import today, history, today_temperature, today_current

from django.urls import path, register_converter

from .classes import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('today/<float:lat>/<float:lon>', today),
    path('today/temperature/<float:lat>/<float:lon>', today_temperature),
    path('today/current/<float:lat>/<float:lon>', today_current),
    path('history/<float:lat>/<float:lon>/<str:start>/<str:end>', history),
]
