#Complexity categories: transport distances (A2), rounds of manufacturing (A3) and transport to waste processing facility (C2) (supersedes Table 4.9 in TM65)
CATEGORY_PRESETS = {
    "category_1_low_complexity": {  # Category 1: low complexity
        "label": "Category 1 - Low complexity",  # human readable label
        "examples": [  # example products to help mapping
            "pipes", "cables", "ducts", "valves", "fire alarm devices", "access control",
            "cable containment", "electrical outlets", "busbar","ductwork", "diffusers",
        ],
        "a2_distance_km": 1500,   # default A2 transport distance (km by truck)
        "a3_rounds_of_manufacture": 1,  # default rounds of manufacture
        "c2_distance_km": 100,    # default C2 transport to waste (km by truck)
    },
    "category_2_medium_complexity": {  # Category 2: medium complexity
        "label": "Category 2 - Medium complexity",
        "examples": [
            "pumps", "luminaires", "control panels", "lighting control devices", "sensors", "thermal store", "bms controller","fan",
        ],
        "a2_distance_km": 3000,   # default A2 transport distance (km by truck)
        "a3_rounds_of_manufacture": 2,  # default rounds of manufacture
        "c2_distance_km": 100,    # default C2 transport to waste (km by truck)
    },
    "category_3_high_complexity": {  # Category 3: high complexity
        "label": "Category 3 - High complexity",
        "examples": [
            "air handling units", "ahu", "chiller", "fcu", "cooling tower", "ducted split", "ahu unit", "heat pump", "boilers", "heat interface units", "MVHR", "switchgear", "UPS","VAV","VAV Box", "VRF Indoor Unit", "VRF Outdoor Unit",
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

def resolve_complexity_category(product_type: str) -> str | None:
    """
    Return the CATEGORY_PRESETS key for a given product_type string.

    Lookup order:
    1) exact match (case-insensitive) against example entries
    2) substring match (case-insensitive) where product_type contains an example or vice-versa
    3) None if no match found
    """
    if not product_type:
        return None
    pt = product_type.strip().lower()

    # exact lookup
    if pt in PRODUCT_TYPE_TO_COMPLEXITY:
        return PRODUCT_TYPE_TO_COMPLEXITY[pt]

    # substring/partial match against examples
    for ex, cat_key in PRODUCT_TYPE_TO_COMPLEXITY.items():
        if pt == ex or pt in ex or ex in pt:
            return cat_key

    return None
# #Table 2.4 Transport emissions factors (Table 4.8 in TM65)
TRANSPORT_EMISSION_FACTOR_A2 = 0.133  # kgCO2e / t·km (BEIS average HGV)
