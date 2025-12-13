# Table 2.8 Transport scenarios: A4 (transport to site) (supersedes Table 4.12 in TM65)
PRESET_A4_SCENARIOS = {
    "australia_within_state_manufactured": {"road_km": 100, "sea_km": 0},        # within state manufactured
    "new_zealand_within_region_manufactured": {"road_km": 100, "sea_km": 0},    # within region manufactured
    "new_zealand_nationally_manufactured": {"road_km": 1000, "sea_km": 0},      # nationally manufactured
    "australia_nationally_manufactured": {"road_km": 2000, "sea_km": 0},        # nationally manufactured
    "australia_nz_globally_manufactured_asia": {"road_km": 300, "sea_km": 10000}, # globally manufactured (Asia)
}

A4_SCENARIOS={}
for key, preset in PRESET_A4_SCENARIOS.items():
    A4_SCENARIOS[key] = {
        "road_km": float(preset.get("road_km", 0.0)),
        "sea_km": float(preset.get("sea_km", 0.0)),
    }
def get_a4_preset(preset_key: str):
    """Return a normalized transport scenario dict for the given preset key.

    Returns a dict with keys `road_km` and `sea_km` as floats. If the preset
    key is not found an empty scenario (0 km) is returned.
    """
    if not preset_key:
        return {"road_km": 0.0, "sea_km": 0.0}
    preset = PRESET_A4_SCENARIOS.get(preset_key)
    if not preset:
        return {"road_km": 0.0, "sea_km": 0.0}
    return {"road_km": float(preset.get("road_km", 0.0)), "sea_km": float(preset.get("sea_km", 0.0))}



TRANSPORT_EMISSION_FACTORS_ROAD = 0.133
TRANSPORT_EMISSION_FACTORS_SEA = 0.02


