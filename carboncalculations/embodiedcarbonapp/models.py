from django.db import models

class EmbodiedCarbon(models.Model):
    product_type = models.CharField(max_length=100)
    weight_kg = models.FloatField()
    electricity_usage_kwh = models.FloatField()
    location_of_factory = models.CharField(max_length=100)
    

