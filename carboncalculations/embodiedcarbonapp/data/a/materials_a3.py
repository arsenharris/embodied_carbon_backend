CATEGORY_PRESETS = {
    "category_1_low_complexity": {  # Category 1: low complexity
        "label": "Category 1 - Low complexity",  # human readable label
        "examples": [  # example products to help mapping
            "pipes", "cables", "ducts", "valves", "fire alarm devices", "access control",
            "cable containment", "electrical outlets", "busbars",
        ],
        "a2_distance_km": 1500,   # default A2 transport distance (km by truck)
        "a3_rounds_of_manufacture": 1,  # default rounds of manufacture
        "c2_distance_km": 100,    # default C2 transport to waste (km by truck)
    },
    "category_2_medium_complexity": {  # Category 2: medium complexity
        "label": "Category 2 - Medium complexity",
        "examples": [
            "pumps", "luminaires", "control panels", "lighting control devices", "sensors", "thermal store",
        ],
        "a2_distance_km": 3000,   # default A2 transport distance (km by truck)
        "a3_rounds_of_manufacture": 2,  # default rounds of manufacture
        "c2_distance_km": 100,    # default C2 transport to waste (km by truck)
    },
    "category_3_high_complexity": {  # Category 3: high complexity
        "label": "Category 3 - High complexity",
        "examples": [
            "air handling units", "ahu", "ahu unit", "Heat pump", "boilers", "heat interface units", "MVHR", "switchgear", "UPS",
        ],
        "a2_distance_km": 6000,   # default A2 transport distance (km by truck)
        "a3_rounds_of_manufacture": 4,  # default rounds of manufacture
        "c2_distance_km": 100,    # default C2 transport to waste (km by truck)
    },
}
PRODUCT_TYPE_TO_COMPLEXITY = {}
for cat_key, preset in CATEGORY_PRESETS.items():
    for ex in preset.get("examples", []):
        PRODUCT_TYPE_TO_COMPLEXITY[ex.lower()] = cat_key


# # Table 2.6 Carbon factors for electricity: A3 (manufacturing) (supersedes Table 4.10 in TM65)
ELECTRICITY_CARBON_FACTORS = {
    "new_south_wales_and_act": 0.85,        # New South Wales & Australian Capital Territory
    "victoria": 1.00,                       # Victoria
    "queensland": 0.92,                     # Queensland
    "south_australia": 0.36,                # South Australia
    "western_australia": 0.69,              # Western Australia
    "tasmania": 0.16,                       # Tasmania
    "northern_territory": 0.58,             # Northern Territory
    "australia_average": 0.81,              # Australia average
    "new_zealand": 0.11,                    # New Zealand
    "china": 0.54,                          # China
    "hong_kong": 0.68,                      # Hong Kong (average)
    "india": 0.71,                          # India
    "japan": 0.47,                          # Japan
    "south_korea": 0.42,                    # South Korea
    "singapore": 0.41,                      # Singapore
    "thailand": 0.48,                       # Thailand
    "asia": 0.84,                           # Asia regional average
    "middle_east": 0.68,                    # Middle East regional average

    # Backwards-compatible keys (optional)
    "China": 0.54,                          # legacy key used elsewhere
    "Australia_average": 0.81,              # legacy key used elsewhere
}

