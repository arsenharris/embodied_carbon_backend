from django.db import models
from django.utils import timezone

class EmbodiedCarbon(models.Model):
    
    project_name = models.CharField(max_length=200)
    product_type = models.CharField(max_length=100)
    weight_kg = models.FloatField()
    location_of_factory = models.CharField(max_length=100)
    lifetime_years = models.FloatField()
    location_of_use = models.CharField(max_length=100)
    electricity_usage_kwh = models.FloatField(blank=True, null=True)
    capacity_kw = models.FloatField(blank=True, null=True)
    refrigerant_used = models.CharField(max_length=100, blank=True, null=True)
    refrigerant_charge_kg = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)