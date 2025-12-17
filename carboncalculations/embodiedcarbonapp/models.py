from django.db import models

class EmbodiedCarbon(models.Model):
    
    project_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=100)
    weight_kg = models.FloatField()
    electricity_usage_kwh = models.FloatField()
    location_of_factory = models.CharField(max_length=100)
    capacity_kw = models.FloatField(blank=True, null=True)
    lifetime_years = models.FloatField(blank=True, null=True)
    refrigerant_used = models.CharField(max_length=100, blank=True, null=True)
    refrigerant_charge_kg = models.FloatField(blank=True, null=True)
    location_of_use = models.CharField(max_length=100, blank=True, null=True)
