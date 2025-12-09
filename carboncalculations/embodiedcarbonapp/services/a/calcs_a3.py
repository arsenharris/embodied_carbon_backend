from ...data.a.materials_a3 import CATEGORY_PRESETS, ELECTRICITY_CARBON_FACTORS,PRODUCT_TYPE_TO_COMPLEXITY
from ...models import EmbodiedCarbon
from typing import Dict, Any  # import typing helpers


def calculate_a3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    if instance is None:
        raise ValueError("instance is required")
    
    product_type = getattr(instance, "product_type", None)
    energy_kwh_per_unit = getattr(instance, "electricity_usage_kwh", None)
    location = getattr(instance, "location_of_factory", None)
    
    if not product_type or energy_kwh_per_unit is None or not location:
        raise ValueError("product_type, electricity_usage_kwh, and location_of_factory are required")
    
    category_key = PRODUCT_TYPE_TO_COMPLEXITY.get(product_type.lower())
    manufacture_preset = CATEGORY_PRESETS.get(category_key)
    if not manufacture_preset:
        raise ValueError(f"No manufacturing preset for product_type '{product_type}'")
    
    rounds_of_manufacture = float(manufacture_preset.get("a3_rounds_of_manufacture", 1.0))
    
    carbon_factor = ELECTRICITY_CARBON_FACTORS.get(location)
    if carbon_factor is None:
        raise ValueError(f"No electricity carbon factor for location '{location}'")
    
    a3_kgco2e = energy_kwh_per_unit * rounds_of_manufacture * carbon_factor
    
    return {
        "product_type": product_type,
        "energy_kwh_per_unit": energy_kwh_per_unit,
        "rounds_of_manufacture": rounds_of_manufacture,
        "manufacture_region": location,
        "electricity_carbon_factor_kg_per_kwh": carbon_factor,
        "a3_kgco2e": a3_kgco2e,
    }