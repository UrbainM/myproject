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
        ('pie', 'Pie Chart'),
        # Add more chart types as needed
    ])
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class DataSet(models.Model):
    visualization = models.ForeignKey(Visualization, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return f"{self.visualization.title} - {self.label}"