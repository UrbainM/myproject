from django.urls import path
from .views import home, chart, visualization, data, add_dataset, seaborn_datasets, get_dataset_api

urlpatterns = [
    path('', home, name='home'),
    path('chart/', chart, name='chart'),
    path('visualization/<str:dataset>/', visualization, name='visualization'),
    path('data/', data, name='data'),
    path('add_dataset/', add_dataset, name='add_dataset'),
    path('seaborn_datasets/', seaborn_datasets, name='seaborn_datasets'),
    path('api/get_dataset/<str:dataset_name>', get_dataset_api, name='get_dataset_api'),
]