from django.urls import path
from .views import today

from django.urls import path, register_converter

from .classes import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')


urlpatterns = [
    path('today/<float:lat>/<float:lon>', today),
]
