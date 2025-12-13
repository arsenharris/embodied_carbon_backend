from ...data.a.materials_a1 import MATERIAL_COEFFS, PRESET_PERCENTAGES, PRESET_PERCENTAGES_NORMALIZED
from ...models import EmbodiedCarbon
from typing import Dict, Any  # import typing helpers

def calculate_a1_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:  # compute A1 using an EmbodiedCarbon model instance
    """
    Calculate the A1 embodied carbon based on total weight and material percentages.
    
    :param total_weight_kg: Total weight of the product in kg
    :param percentages: Dictionary of material percentages (material_name: percentage)
    :return: Total A1 embodied carbon in kg CO2e
    """
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance

    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    if total_weight_kg is None:  # ensure weight exists
        raise ValueError("instance.weight_kg is required")  # error if missing
    
    # Priority: if the instance has an in-memory override (set by the view), use that
    preset_percentages = getattr(instance, 'materials_override', None)
    # Try exact lookup first, then fallback to case-insensitive mapping from built-in presets
    if not preset_percentages:
        preset_percentages = PRESET_PERCENTAGES.get(product_type)
    if not preset_percentages:
        preset_percentages = PRESET_PERCENTAGES_NORMALIZED.get(product_type.lower())
    if not preset_percentages:
        raise ValueError(f"No preset percentages for product_type '{product_type}'")  # error if missing

    # Validate preset percentages: ensure they are numeric and do not exceed 100% total
    try:
        total_percent = sum(float(v or 0.0) for v in preset_percentages.values())
    except Exception:
        raise ValueError(f"Invalid preset percentages for product_type '{product_type}'; all percentages must be numeric")

    if total_percent > 100.0001:  # small tolerance for floating-point
        raise ValueError(f"Preset percentages sum to {total_percent:.2f}% (>100%) for product_type '{product_type}'")
    # Enforce a sensible minimum coverage to avoid large unspecified remaining mass
    if total_percent < 95.0 - 0.0001:
        raise ValueError(f"Preset percentages sum to {total_percent:.2f}% (<95%) for product_type '{product_type}'")

    weights: Dict[str, float] = {}  # will hold computed material weights (kg)
    a1_components: Dict[str, float] = {}  # will hold computed material embodied carbon (kg CO2e)
    total_weight_accounted: float = 0.0  # running total of weight accounted by preset percentages
    total_a1: float = 0.0  # running total of A1 embodied carbon

    # iterate preset materials and compute each material contribution
    for material, percentage in preset_percentages.items():  # loop each material and its percentage
        material_percentage = float(percentage or 0.0)  # ensure percentage is a float
        material_weight = float(total_weight_kg) * (material_percentage / 100.0)  # compute material weight in kg
        material_coeff = float(MATERIAL_COEFFS.get(material, MATERIAL_COEFFS.get("steel", 0.0)))  # lookup coefficient (fallback to steel)
        material_a1 = material_weight * material_coeff  # compute embodied carbon for this material (kgCO2e)

        weights[material] = material_weight  # store material weight
        a1_components[material] = material_a1  # store material A1 contribution

        total_weight_accounted += material_weight  # accumulate accounted weight
        total_a1 += material_a1  # accumulate total A1

    remaining_weight = max(0.0, float(total_weight_kg) - total_weight_accounted)  # compute any unaccounted remaining weight
    if remaining_weight > 0.0:
        # Attribute any small remaining mass to `steel` (merge with existing steel entry)
        steel_coeff = float(MATERIAL_COEFFS.get("steel", 0.0))
        remaining_a1 = remaining_weight * steel_coeff
        weights["steel"] = weights.get("steel", 0.0) + remaining_weight
        a1_components["steel"] = a1_components.get("steel", 0.0) + remaining_a1
        total_a1 += remaining_a1

    return {  # return structured result
        "total_a1": total_a1,  # total A1 embodied carbon (kgCO2e)
    }