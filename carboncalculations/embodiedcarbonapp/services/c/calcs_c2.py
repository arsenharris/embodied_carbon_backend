from ...data.c.materials_c2 import CATEGORY_PRESETS, TRANSPORT_EMISSION_FACTOR_C2, PRODUCT_TYPE_TO_COMPLEXITY
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon

def calculate_c2_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """Calculate C2 transport emissions (kg CO2e).

    Args:
    product_weight_kg: product mass in kilograms.
    product_type: optional product type/name used to choose a category preset
        (will search `CATEGORY_PRESETS[..]["examples"]`). If not provided or
        not found, the first category preset will be used as a fallback.
    transport_factor: emission factor in kgCO2e / (t·km). If not provided,
        `TRANSPORT_EMISSION_FACTOR_C2` is used.

    Returns:
    float: C2 emissions in kg CO2e.
    """
    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)  # get product type from model
    weight_kg = getattr(instance, "weight_kg", None)        # get weight (kg) from model
    
    if product_type is None:
        raise ValueError("instance.product_type is required")
    if weight_kg is None:
        raise ValueError("instance.weight_kg is required")

    # determine category and distance
    category_key = PRODUCT_TYPE_TO_COMPLEXITY.get(product_type)
    if category_key is None:
        # fallback to the first preset in the dict
        category_key = next(iter(CATEGORY_PRESETS))
    distance_km = CATEGORY_PRESETS[category_key].get("c2_distance_km", 0)
    weight_t = float(weight_kg) / 1000.0  # convert kg to tonnes
    total_c2 = weight_t * float(distance_km) * TRANSPORT_EMISSION_FACTOR_C2  
    return {
        "total_c2": total_c2,
    }