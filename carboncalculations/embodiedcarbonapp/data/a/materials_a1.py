#Table 2.3 Embodied carbon coefficients (Table 2.1 in TM65)
MATERIAL_COEFFS = {
    "abs": 3.76,
    "aluminium": 13.1,
    "brass": 4.8,
    "cast_iron": 1.52,
    "ceramic": 0.7,
    "copper": 3.81,
    "expanded_polystyrene": 3.43,
    "glass": 1.44,
    "insulation": 1.86,
    "iron": 2.03,
    "lithium": 5.3,
    "plastics": 3.31,
    "polyamide": 9.14,
    "polycarbonates": 7.62,
    "polyethylene": 2.53,
    "polyurethane_foam": 4.55,
    "pvc": 3.1,
    "rubber": 2.85,
    "silicon": 13.8,
    "stainless_steel": 4.4,
    "steel": 2.97,
    "zinc": 4.18,
    "electronic_components": 49.0,
    "printed_wiring_board_mixed_mounted": 154.0,
}

PRESET_PERCENTAGES = {
    "Heat pump": {
        "plastics": 4, 
        "stainless_steel": 10, 
        "aluminium": 7, 
        "brass": 1, 
        "steel": 60,
        "copper": 10,
        "electronic_components": 3,
    },
    "Chiller": {
        "steel": 40, "aluminium": 8, "copper": 10, "plastics": 8,
        "stainless_steel": 6, "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, "glass": 1, "rubber": 3,
        "pvc": 4, "polyurethane_foam": 5, "polyethylene": 2, "polycarbonates": 3,
        "polyamide": 1, "abs": 2, "zinc": 1, "ceramic": 0.5, "iron": 1,
        "expanded_polystyrene": 0.5, "lithium": 0.1, "silicon": 0.2, "cast_iron": 0.5,
    },
    "Ducted split": {
        "steel": 30, "aluminium": 12, "copper": 9, "plastics": 12,
        "stainless_steel": 4, "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, "glass": 1, "rubber": 3,
        "pvc": 5, "polyurethane_foam": 6, "polyethylene": 3, "polycarbonates": 3,
        "polyamide": 1, "abs": 4, "zinc": 1, "ceramic": 0.5, "iron": 1,
        "expanded_polystyrene": 0.5, "lithium": 0.1, "silicon": 0.2, "cast_iron": 0.5,
    },
}


