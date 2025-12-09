# Table 2.8 Transport scenarios: A4 (transport to site) (supersedes Table 4.12 in TM65)
PRESET_A4_SCENARIOS = {
    "australia_within_state_manufactured": {"road_km": 100, "sea_km": 0},        # within state manufactured
    "new_zealand_within_region_manufactured": {"road_km": 100, "sea_km": 0},    # within region manufactured
    "new_zealand_nationally_manufactured": {"road_km": 1000, "sea_km": 0},      # nationally manufactured
    "australia_nationally_manufactured": {"road_km": 2000, "sea_km": 0},        # nationally manufactured
    "australia_nz_globally_manufactured_asia": {"road_km": 300, "sea_km": 10000}, # globally manufactured (Asia)
}

TRANSPORT_EMISSION_FACTORS = {
    "A2": {
        "mode": "road",
        "value_kgCO2e_per_tkm": 0.133,
        "description": "An average heavy goods vehicle (HGV) with average load, includes well-to-tank (WTT) emissions.",
        "source": "Government GHG conversion factors for 2021 (BEIS, 2022)"
    },
    "A4_road": {
        "mode": "road",
        "value_kgCO2e_per_tkm": 0.133,
        "description": "An average heavy goods vehicle (HGV) with average load, includes WTT emissions.",
        "source": "Government GHG conversion factors for 2021 (BEIS, 2022)"
    },
    "A4_sea": {
        "mode": "sea",
        "value_kgCO2e_per_tkm": 0.020,
        "description": "An average container ship, includes well-to-tank (WTT) emissions.",
        "source": "Government GHG conversion factors for 2021 (BEIS, 2022)"
    },
    "C2": {
        "mode": "road",
        "value_kgCO2e_per_tkm": 0.133,
        "description": "An average heavy goods vehicle (HGV) with average load, includes WTT emissions.",
        "source": "Government GHG conversion factors for 2021 (BEIS, 2022)"
    }
}
