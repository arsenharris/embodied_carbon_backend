from ...data.a.materials_a2 import CATEGORY_PRESETS, TRANSPORT_EMISSION_FACTOR_A2,PRODUCT_TYPE_TO_COMPLEXITY
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon


def calculate_a2_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """
    Calculate A2 (transport to site) using the saved model instance:
      A2 = (weight in tonnes) * distance_km * emission_factor (kgCO2e / t·km)
    Returns a dict with distance_km, weight_tonnes and a2_kgco2e
    """
    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)  # get product type from model
    weight_kg = getattr(instance, "weight_kg", None)        # get weight (kg) from model
    if product_type is None:
        raise ValueError("instance.product_type is required")
    if weight_kg is None:
        raise ValueError("instance.weight_kg is required")

    # 1) try direct mapping product_type -> category key
    category_key = PRODUCT_TYPE_TO_COMPLEXITY.get(product_type)

    # 2) fallback: search examples lists (case-insensitive, allow substring match)
    if not category_key:
        pt_lower = product_type.lower()
        for key, preset in CATEGORY_PRESETS.items():
            for example in preset.get("examples", []):
                ex = example.lower()
                if pt_lower == ex or pt_lower in ex or ex in pt_lower:
                    category_key = key
                    break
            if category_key:
                break

    if not category_key:
        raise ValueError(f"No transport preset for product_type '{product_type}'")

    distance_km = float(CATEGORY_PRESETS[category_key].get("a2_distance_km", 0.0))  # km to transport
    weight_tonnes = float(weight_kg) / 1000.0                         # convert kg -> t
    emission_factor = float(TRANSPORT_EMISSION_FACTOR_A2)            # kgCO2e / t·km

    a2_kgco2e = weight_tonnes * distance_km * emission_factor        # compute A2

    return {
        "a2_kgco2e": a2_kgco2e,
    }  