from django.test import TestCase
from django.urls import reverse
from .models import SeabornDataset

class SeabornDatasetAPITests(TestCase):
    def setUp(self):
        # Create a SeabornDataset for testing
        self.test_dataset = SeabornDataset.objects.create(
            name='test_dataset',
            data=[
                {'label': 'Label 1', 'value': 10},
                {'label': 'Label 2', 'value': 20},
                {'label': 'Label 3', 'value': 30},
            ]
        )

    def test_get_dataset_api_success(self):
        # Test the API response for an existing dataset
        url = reverse('get_dataset_api', kwargs={'dataset_name': 'test_dataset'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'labels': ['Label 1', 'Label 2', 'Label 3'], 'values': [10, 20, 30]}
        )

    def test_get_dataset_api_not_found(self):
        # Test the API response for a non-existing dataset
        url = reverse('get_dataset_api', kwargs={'dataset_name': 'nonexistent_dataset'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            str(response.content, encoding='utf8'),
            {'error': 'Dataset not found'}
        )