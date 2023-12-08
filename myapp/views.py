# myapp/views.py
from django.shortcuts import render
from .models import DataPoint, Visualization, DataSet

def home(request):
    return render(request, 'home.html')

def chart(request):
    data = DataPoint.objects.all()
    return render(request, 'chart.html', {'data': data})

def visualization(request):
    data = Visualization.objects.all()
    return render(request, 'visualization.html', {'data': data})

def data(request):
    data = DataSet.objects.all()
    return render(request, 'data.html', {'data': data})