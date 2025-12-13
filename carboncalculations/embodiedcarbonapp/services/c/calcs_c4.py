from ...data.c.materials_c4 import LANDFILL_EMISSION_FACTOR, PRODUCT_TYPE_TO_COMPLEXITY
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon


def calculate_c4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """Calculate C4 (end-of-life landfill) emissions (kg CO2e).

    Uses `resolve_end_of_life` to determine an appropriate `landfill_pct`
    for the given `instance.product_type`. If no preset is found the
    landfill percentage defaults to 0. The landfill emission factor is
    taken from `LANDFILL_EMISSION_FACTOR`.
    """
    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)  # get product type from model
    weight_kg = getattr(instance, "weight_kg", None)        # get weight (kg) from model
    if product_type is None:
        raise ValueError("instance.product_type is required")
    if weight_kg is None:
        raise ValueError("instance.weight_kg is required")
    landfill_factor = float(LANDFILL_EMISSION_FACTOR)  # kgCO2e / kg waste

    # lookup mapping case-insensitively; presets store percentages (e.g. 50 == 50%)
    landfill_pct = PRODUCT_TYPE_TO_COMPLEXITY.get(product_type.strip().lower())

    # If not found, default to 0% (no landfill emissions). Convert percent -> fraction.
    if landfill_pct is None:
        landfill_fraction = 0.0
    else:
        landfill_fraction = float(landfill_pct) / 100.0

    c4_kgco2e = float(weight_kg) * landfill_factor * landfill_fraction

    return {
        "c4_kgco2e": c4_kgco2e,
    }
