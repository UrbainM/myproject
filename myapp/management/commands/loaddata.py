# myapp/management/commands/load_seaborn_datasets.py
from django.core.management.base import BaseCommand
from myapp.models import SeabornDataset
import seaborn as sns
import json

class Command(BaseCommand):
    help = 'Load Seaborn datasets into the database'

    def handle(self, *args, **kwargs):
        datasets = sns.get_dataset_names()

        for dataset_name in datasets:
            # Get or create the dataset
            dataset, created = SeabornDataset.objects.get_or_create(name=dataset_name)
            
            if not created:
                # If the dataset already existed, update its data
                data = sns.load_dataset(dataset_name)
                data_json = data.to_json(orient='records')
                dataset.data = json.loads(data_json)
                dataset.save()

        self.stdout.write(self.style.SUCCESS('Seaborn datasets loaded successfully.'))
