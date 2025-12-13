from django.db import models

class EmbodiedCarbon(models.Model):
    product_type = models.CharField(max_length=100)
    weight_kg = models.FloatField()
    electricity_usage_kwh = models.FloatField()
    location_of_factory = models.CharField(max_length=100)
    lifetime_years = models.FloatField(blank=True, null=True)
    REFRIGERANTA_CHOICE=[
        ('R-410A', 'R-410A'),
        ('R-32', 'R-32'),
        ('R-134a', 'R-134a'),
        ('R-407C', 'R-407C'),
        ('R-290', 'R-290'),
        ('R11', 'R11'),
        ('R22', 'R22'),
        ('R600a', 'R600a'),
        ('R744', 'R744'),
        ('R717', 'R717'),    
        ('R718','R718'),
        ('R1234yf','R1234yf'),
        ('R1234ze','R1234ze'),
    ]
    refrigerant_used = models.CharField(max_length=100, choices=REFRIGERANTA_CHOICE, blank=True, null=True)
    refrigerant_charge_kg = models.FloatField(blank=True, null=True)
    CHOICE_REGION = [
        ('australia_within_state_manufactured', 'australia_within_state_manufactured'),
        ('australia_nationally_manufactured', 'australia_nationally_manufactured'),
        ('new_zealand_within_region_manufactured', 'new_zealand_within_region_manufactured'),
        ('new_zealand_nationally_manufactured', 'new_zealand_nationally_manufactured'),
        ("australia_nz_globally_manufactured_asia", "australia_nz_globally_manufactured_asia"),
    ]
    location_of_use = models.CharField(max_length=100, choices=CHOICE_REGION)