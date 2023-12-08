# myapp/views.py
import os, base64
import json
from io import BytesIO

import seaborn as sns
import matplotlib.pyplot as plt

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import DataPoint, DataSet, Visualization, SeabornDataset
from .forms import DatasetForm, SeabornDatasetForm

# Assuming the datasets are stored as JSON files in /myapp/datasets
DATASETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'datasets')

def home(request):
    return render(request, 'home.html')

def chart(request):
    data = DataPoint.objects.all()
    return render(request, 'chart.html', {'data': data})

def visualization(request):
    dataset_id = request.GET.get('dataset')
    dataset = get_object_or_404(DataSet, id=dataset_id)

    labels = dataset.labels.split(',')
    values = dataset.values

    context = {
        'dataset': dataset,
        'labels': labels,
        'values': values,
    }

    return render(request, 'visualization.html', context)

def data(request):
    if request.method == 'POST':
        selected_dataset_id = request.POST.get('dataset')
        if selected_dataset_id:
            return redirect('visualization', dataset_id=selected_dataset_id)
    datasets = DataSet.objects.all()
    return render(request, 'data.html', {'datasets': datasets})

def get_dataset(request):
    if request.method == 'POST':
        dataset_id = request.POST.get('dataset_id')
        dataset = get_object_or_404(DataSet, pk=dataset_id)

        # Load dataset from JSON file in /myapp/datasets
        dataset_path = os.path.join(DATASETS_DIR, f'{dataset.name}.json')
        with open(dataset_path, 'r') as file:
            data = json.load(file)

        return JsonResponse({'data': data})

    return JsonResponse({'error': 'Invalid request method'})

def add_dataset(request):
    if request.method == 'POST':
        form = DatasetForm(request.POST)
        if form.is_valid():
            # Save dataset to a JSON file in /myapp/datasets
            dataset = form.save()
            dataset_path = os.path.join(DATASETS_DIR, f'{dataset.name}.json')
            with open(dataset_path, 'w') as file:
                json.dump([], file)
            return redirect('visualization')
    else:
        form = DatasetForm()

    return render(request, 'add_dataset.html', {'form': form})

def seaborn_datasets(request):
    datasets = SeabornDataset.objects.all()
    return render(request, 'seaborn_datasets.html', {'datasets' : datasets})

def get_dataset_api(request, dataset_name):
    try:
        dataset = SeabornDataset.objects.get(name=dataset_name)
        data = dataset.data

        # Assuming data is a list of dictionaries
        labels = [item for item in data]
        values = [values for values in data]

        return JsonResponse({'labels': labels, 'values': values})
    except SeabornDataset.DoesNotExist:
        return JsonResponse({'error': 'Dataset not found'}, status=404)