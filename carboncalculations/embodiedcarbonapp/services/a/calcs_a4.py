from ...data.a.materials_a4 import PRESET_A4_SCENARIOS, TRANSPORT_EMISSION_FACTORS_ROAD, TRANSPORT_EMISSION_FACTORS_SEA,get_a4_preset
from ...models import EmbodiedCarbon
from typing import Dict, Any  # import typing helpers


def calculate_a4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:

    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)
    weight_kg = getattr(instance, "weight_kg", None)
    location_of_use = getattr(instance, "location_of_use", None)
    preset_key = getattr(instance, "location_of_use", None)


    if product_type is None:
        raise ValueError("instance.product_type is required")
    if weight_kg is None:
        raise ValueError("instance.weight_kg is required")
    weight_t = float(weight_kg) / 1000.0


    scenario = get_a4_preset(preset_key)
    road_km = scenario["road_km"]
    sea_km = scenario["sea_km"]

    if preset_key in [
            "australia_within_state_manufactured",
            "new_zealand_within_region_manufactured",
            "new_zealand_nationally_manufactured",
            "australia_nationally_manufactured"
        ]:
            distance_factor = road_km * TRANSPORT_EMISSION_FACTORS_ROAD
    else:
            distance_factor = (road_km * TRANSPORT_EMISSION_FACTORS_ROAD) + (sea_km * TRANSPORT_EMISSION_FACTORS_SEA)

    total_a4= weight_t * distance_factor


    return {
        "total_a4_kgco2e": total_a4,
        "total_a4": total_a4,
        "product": product_type,
        "weight_kg": weight_kg,
        "location_of_use": location_of_use,
        "preset_key": preset_key,
        "road_km": road_km,
        "sea_km": sea_km,
    }