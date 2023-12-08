from django.core.management.base import BaseCommand
from myapp.models import SeabornDataset
import seaborn as sns

class Command(BaseCommand):
    help = 'Load Seaborn datasets into the database'

    def handle(self, *args, **kwargs):
        datasets = sns.get_dataset_names()
        for dataset_name in datasets:
            try:
                description = sns.load_dataset(dataset_name).__doc__
                SeabornDataset.objects.create(name=dataset_name, description=description)
                self.stdout.write(self.style.SUCCESS(f'Successfully loaded dataset: {dataset_name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error loading dataset {dataset_name}: {str(e)}'))
