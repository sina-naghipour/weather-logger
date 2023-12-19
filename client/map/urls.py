from django.urls import path, register_converter
from .views import Map
from .classes import FloatUrlParameterConverter

register_converter(FloatUrlParameterConverter, 'float')
urlpatterns = [
    path('/<float:lat>/<float:lon>/', Map.as_view()),

]