from typing import Dict, Any

from ..data.materials_b1andc1 import REFRIGERANT_LEAKAGE_SCENARIOS, REFRIGERANT_GWP
from ..models import EmbodiedCarbon


def calculate_b1andc1_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    """Calculate B1 (use-phase refrigerant leakage over lifetime) and
    C1 (end-of-life refrigerant leakage) emissions for an EmbodiedCarbon
    instance.

    Formula (B1):
        b1 = refrigerant_charge_kg * leakage_rate_b1_per_year * lifetime_years * gwp_100yr

    Formula (C1):
        c1 = refrigerant_charge_kg * end_of_life_leakage_rate * gwp_100yr

    The leakage rates are selected from `REFRIGERANT_LEAKAGE_SCENARIOS` based on
    whether `refrigerant_charge_kg` is > 100 kg (type A) or <= 100 kg (type B).
    """
    if instance is None:
        raise ValueError("instance is required")

    # Required fields on the model
    refrigerant_used = getattr(instance, "refrigerant_used", None)
    refrigerant_charge_kg = getattr(instance, "refrigerant_charge_kg", None)
    lifetime_years = getattr(instance, "lifetime_years", None)

    if refrigerant_used is None:
        raise ValueError("instance.refrigerant_used is required")
    if refrigerant_charge_kg is None:
        raise ValueError("instance.refrigerant_charge_kg is required")
    if lifetime_years is None:
        raise ValueError("instance.lifetime_years is required")

    # Normalize refrigerant codes for robust matching (accepts variants like "R-410A")
    def _normalize(code: str) -> str:
        return "".join(ch for ch in (code or "") if ch.isalnum()).lower()

    gwp_map = { _normalize(item.get("refrigerant")): item for item in REFRIGERANT_GWP }
    key = _normalize(refrigerant_used)
    gwp_entry = gwp_map.get(key)
    if gwp_entry is None:
        available = ", ".join(sorted([item.get("refrigerant") for item in REFRIGERANT_GWP]))
        raise ValueError(
            f"Unknown refrigerant: {refrigerant_used}. Available refrigerants: {available}"
        )
    gwp_100yr = float(gwp_entry["gwp_100yr"])

    # Select leakage scenario by charge size (>100 kg => type A, else type B)
    if refrigerant_charge_kg > 100:
        # Prefer explicit match for 'greater' entry, fallback to first
        scenario = next(
            (s for s in REFRIGERANT_LEAKAGE_SCENARIOS if "greater" in s.get("product_type", "").lower()),
            REFRIGERANT_LEAKAGE_SCENARIOS[0],
        )
    else:
        scenario = next(
            (s for s in REFRIGERANT_LEAKAGE_SCENARIOS if "less" in s.get("product_type", "").lower()),
            REFRIGERANT_LEAKAGE_SCENARIOS[-1],
        )

    leakage_rate_b1_per_year = float(scenario.get("annual_leakage_rate_b1_use", 0.0))
    end_of_life_leakage_rate = float(scenario.get("end_of_life_leakage_rate_c1_deconstruction", 0.0))

    # B1: total leaked over lifetime
    total_leakage_b1_kg = refrigerant_charge_kg * leakage_rate_b1_per_year * lifetime_years
    b1_emissions_kgco2eq = total_leakage_b1_kg * gwp_100yr

    # C1: end-of-life leakage applied once at deconstruction
    c1_emissions_kgco2eq = refrigerant_charge_kg * end_of_life_leakage_rate * gwp_100yr

    return {
        "b1_emissions_kgco2eq": b1_emissions_kgco2eq,
        "c1_emissions_kgco2eq": c1_emissions_kgco2eq,
        "gwp_100yr": gwp_100yr,
        "leakage_rate_b1_per_year": leakage_rate_b1_per_year,
        "end_of_life_leakage_rate": end_of_life_leakage_rate,
        "total_leakage_b1_kg": total_leakage_b1_kg,
    }