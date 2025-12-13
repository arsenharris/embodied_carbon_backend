from ...data.c.materials_c3 import ELECTRICITY_CARBON_FACTORS
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon


def calculate_c3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """Calculate C3 (waste processing / electricity use) emissions (kg CO2e).

    Args:
    product_weight_kg: product mass in kilograms.
    product_type: optional product type/name used to choose a category preset
        (will search `CATEGORY_PRESETS[..]["examples"]`). If not provided or
        not found, the first category preset will be used as a fallback.
    transport_factor: emission factor in kgCO2e / (t·km). If not provided,
        `TRANSPORT_EMISSION_FACTOR_C2` is used.

    Returns:
    float: C3 emissions in kg CO2e.
    """
    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)  # get product type from model
    energy_kwh_per_unit = getattr(instance, "electricity_usage_kwh", None)
    location = getattr(instance, "location_of_factory", None)

    if product_type is None:
        raise ValueError("instance.product_type is required")

    # determine category and distance
    c3_carbon_factor = ELECTRICITY_CARBON_FACTORS.get(location)
    c3 = energy_kwh_per_unit * c3_carbon_factor
    return {
        "c3_kgco2e": c3,
    }