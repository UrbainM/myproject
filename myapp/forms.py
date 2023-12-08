from django import forms
from .models import DataSet
import seaborn as sns

class DatasetForm(forms.ModelForm):
    class Meta:
        model = DataSet
        fields = ['name']

class SeabornDatasetForm(forms.Form):
    dataset_choices = [(dataset, dataset) for dataset in sns.get_dataset_names()]

    dataset = forms.ChoiceField(choices=dataset_choices, widget=forms.Select(attrs={'class': 'form-select'}))