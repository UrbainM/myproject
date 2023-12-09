import os
import json

import seaborn as sns

from django.http import JsonResponse, Http404
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



def visualization(request, dataset):
    try:
        # Load the selected dataset using Seaborn
        data = sns.load_dataset(dataset)

        # Check if the dataset is empty
        if data.empty:
            raise ValueError(f"The {dataset} dataset is empty.")

        # Get column names for dynamic visualization options
        column_names = data.columns.tolist()

        if request.method == 'POST':
            selected_column = request.POST.get('column')

            # Check if the selected column exists in the dataset
            if selected_column not in column_names:
                raise ValueError(f"The selected column '{selected_column}' does not exist in the {dataset} dataset.")

            # Create a chart based on the user-selected column
            chart_data = data[selected_column].value_counts().reset_index()
            chart_data.columns = ['label', 'value']

            chart_config = {
                'type': 'bar',
                'data': {
                    'labels': chart_data['label'].tolist(),
                    'datasets': [{
                        'label': selected_column,
                        'data': chart_data['value'].tolist(),
                        'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                        'borderColor': 'rgba(75, 192, 192, 1)',
                        'borderWidth': 1
                    }]
                },
                'options': {
                    'scales': {
                        'y': {
                            'beginAtZero': True
                        }
                    }
                }
            }

            chart_json = json.dumps(chart_config)

            return render(request, 'visualization.html', {'chart_json': chart_json, 'column_names': column_names})

        return render(request, 'visualization.html', {'column_names': column_names})
    except Exception as e:
        # Handle errors e.g. if the dataset is not found
        return render(request, 'error.html', {'error_message': str(e)})
    


def data(request):
    # Get a list of all Seaborn's built-in datasets
    dataset_names = sns.get_dataset_names()

    if request.method == 'POST':
        selected_dataset = request.POST.get('dataset')
        if selected_dataset in dataset_names:
            # Redirect to the visualization page with the selected dataset name
            return redirect('visualization', dataset=selected_dataset)
        else:
            raise Http404(f'Dataset "{selected_dataset}" not found.')

    return render(request, 'data.html', {'dataset_names': dataset_names})





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

        labels = [row.get('label') for row in data]
        values = [row.get('value') for row in data]

        return JsonResponse({'labels': labels, 'values': values})
    except SeabornDataset.DoesNotExist:
        return JsonResponse({'error': 'Dataset not found'}, status=404)