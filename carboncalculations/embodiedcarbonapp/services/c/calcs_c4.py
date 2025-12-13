from ...data.c.materials_c4 import END_OF_LIFE_PRESETS, LANDFILL_EMISSION_FACTOR
from typing import Dict, Any  # import typing helpers
from ...models import EmbodiedCarbon


def calculate_c4_from_instance(weight_kg: float, landfill_pct: float = None, landfill_factor: float = None) -> float:
    """Calculate C4 landfill emissions (kg CO2e).

    weight_kg: total product mass in kg
    landfill_pct: percentage (0-100) of mass sent to landfill
    landfill_factor: kg CO2e per kg waste (if None, uses materials_c4.LANDFILL_EMISSION_FACTOR)
    """
    if weight_kg is None:
        return 0.0

    if landfill_factor is None:
        landfill_factor = LANDFILL_EMISSION_FACTOR

    mass_to_landfill_kg = float(weight_kg) * float(landfill_factor)
    return mass_to_landfill_kg
