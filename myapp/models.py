from django.db import models

# Create your models here.
class DataPoint(models.Model):
    label = models.CharField(max_length=255)
    value = models.FloatField()
    
class Visualization(models.Model):
    title = models.CharField(max_length=255)
    chart_type = models.CharField(max_length=50, choices=[
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart')
    ])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class DataSet(models.Model):
    labels = models.CharField(default='default_label', max_length=255)
    name = models.CharField(max_length=255)
    values = models.FloatField()

    
class SeabornDataset(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    data = models.JSONField(default=None)