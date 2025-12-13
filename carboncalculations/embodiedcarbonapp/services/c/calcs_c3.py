from ...data.c.materials_c3 import ELECTRICITY_CARBON_FACTORS
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon

def calculate_c3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """Calculate C3 (waste processing) emissions (kg CO2e).

    Args:
    instance: EmbodiedCarbon model instance.

    Returns:
    Dict[str, Any]: Dictionary with C3 emissions in kg CO2e.
    """
    if instance is None:
        raise ValueError("instance is required")

    weight_kg = getattr(instance, "weight_kg", None)        # get weight (kg) from model
    electricity_kwh_per_kg = getattr(instance, "c3_electricity_kwh_per_kg", None)  # get electricity use (kWh/kg) from model

    if weight_kg is None:
        raise ValueError("instance.weight_kg is required")
    if electricity_kwh_per_kg is None:
        raise ValueError("instance.c3_electricity_kwh_per_kg is required")

    electricity_factor = ELECTRICITY_CARBON_FACTORS.get("grid_average", 0.0)  # default to grid average

    c3_kgco2e = float(electricity_kwh_per_kg) * float(electricity_factor)

    return {
        "c3_kgco2e": c3_kgco2e,
    }