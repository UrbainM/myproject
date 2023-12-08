from django.urls import path
from .views import home, chart, visualization, data

urlpatterns = [
    path('', home, name='home'),
    path('chart/', chart, name='chart'),
    path('visualization/', visualization, name='visualization'),
    path('data/', data, name='data'),
]
