from ...data.a.materials_a4 import PRESET_A4_SCENARIOS,TRANSPORT_EMISSION_FACTORS
from ...models import EmbodiedCarbon
from typing import Dict, Any  # import typing helpers


def calculate_a4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:

    if instance is None:
        raise ValueError("instance is required")
    
    product_type = getattr(instance, "product_type", None)
    total_weight_kg = getattr(instance, "weight_kg", None)
    location_of_factory = getattr(instance, "location_of_factory", "overseas")  # default to overseas
    region_of_use = getattr(instance, "region_of_use", "australia")

    if product_type is None:
        raise ValueError("instance.product_type is required")
    if total_weight_kg is None:
        raise ValueError("instance.weight_kg is required")
    
# For now, assume overseas manufacture if location is not very specific
    preset_key = "australia_nz_globally_manufactured_asia"
    transport_scenario = PRESET_A4_SCENARIOS.get(preset_key)
    if not transport_scenario:
        raise ValueError(f"No transport scenario for key '{preset_key}'")
    
    road_km = transport_scenario.get("road_km", 0)
    sea_km = transport_scenario.get("sea_km", 0)
    
    # Get emission factors
    road_factor = TRANSPORT_EMISSION_FACTORS["A4_road"]["value_kgCO2e_per_tkm"]
    sea_factor = TRANSPORT_EMISSION_FACTORS["A4_sea"]["value_kgCO2e_per_tkm"]
    
    # Convert weight to tons
    weight_t = total_weight_kg / 1000.0
    
    # Calculate emissions
    a4_road_kgco2e = weight_t * road_km * road_factor
    a4_sea_kgco2e = weight_t * sea_km * sea_factor
    total_a4_kgco2e = a4_road_kgco2e + a4_sea_kgco2e
    
    return {
        "total_a4_kgco2e": total_a4_kgco2e,
    }