
#Table 2.3 Embodied carbon coefficients (Table 2.1 in TM65) Embodied carbon coefficient (kgCO2e/kg)*
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

# This is for a1 proportion of material.User can override on front end if they want to change the default percentages.
PRESET_PERCENTAGES = {
    "AHU": {
        "steel": 45, "aluminium": 15, "copper": 10,
        "plastics": 8, "insulation": 12,
        "stainless_steel": 3, "electronic_components": 2,
        "pvc": 2, "rubber": 2, "polyurethane_foam": 1,
    },

    "Access Control Device": {
        "plastics": 25,
        "electronic_components": 35,
        "printed_wiring_board_mixed_mounted": 20,
        "copper": 10,
        "steel": 5,
        "aluminium": 5,
    },

    "BMS Controller": {
        "plastics": 20,
        "electronic_components": 35,
        "printed_wiring_board_mixed_mounted": 35,
        "copper": 10,
    },

    "Boiler": {
        "steel": 60, "cast_iron": 20,
        "copper": 5, "stainless_steel": 5,
        "plastics": 3, "rubber": 2,
        "electronic_components": 3,
        "pvc": 2,
    },

    "Busbar": {
        "copper": 70,
        "steel": 20,
        "plastics": 10,
    },

    "Cable Containment": {  # tray, ladder
        "steel": 85,
        "aluminium": 10,
        "zinc": 5,
    },

    "Cables": {
        "copper": 55,
        "pvc": 35,
        "plastics": 10,
    },

    "Chiller": {
        "steel": 40, "aluminium": 8, "copper": 10, "plastics": 8,
        "stainless_steel": 6, "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, "glass": 1, "rubber": 3,
        "pvc": 4, "polyurethane_foam": 5, "polyethylene": 2, "polycarbonates": 3,
        "polyamide": 1, "abs": 2, "zinc": 1, "ceramic": 0.5, "iron": 1,
        "expanded_polystyrene": 0.5, "lithium": 0.1, "silicon": 0.2, "cast_iron": 0.5,
    },

    "Control Panel": {
        "steel": 50,
        "copper": 20,
        "plastics": 10,
        "electronic_components": 15,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "Cooling Tower": {
        "plastics": 40,  # FRP ≈ plastics
        "steel": 35,
        "copper": 5,
        "stainless_steel": 5,
        "rubber": 5,
        "electronic_components": 2,
        "polyurethane_foam": 3,
    },

    "Ducted split": {
        "steel": 30, "aluminium": 12, "copper": 9, "plastics": 12,
        "stainless_steel": 4, "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, "glass": 1, "rubber": 3,
        "pvc": 5, "polyurethane_foam": 6, "polyethylene": 3, "polycarbonates": 3,
        "polyamide": 1, "abs": 4, "zinc": 1, "ceramic": 0.5, "iron": 1,
        "expanded_polystyrene": 0.5, "lithium": 0.1, "silicon": 0.2, "cast_iron": 0.5,
    },

    "Ductwork": {
        "steel": 80,
        "insulation": 12,
        "adhesive": 0,  # unused, but left as-is
        "pvc": 3,
        "rubber": 2,
        "polyurethane_foam": 3,
    },

    "Diffuser": {
        "aluminium": 75,
        "steel": 15,
        "plastics": 5,
        "rubber": 2,
        "stainless_steel": 3,
    },

    "Electrical Outlet": {
        "plastics": 40,
        "copper": 30,
        "steel": 15,
        "electronic_components": 10,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "Fan": {
        "steel": 55,
        "aluminium": 10,
        "copper": 20,
        "plastics": 10,
        "stainless_steel": 3,
        "electronic_components": 2,
    },

    "FCU": {
        "steel": 40, "aluminium": 10, "copper": 20,
        "plastics": 10, "insulation": 10,
        "stainless_steel": 3, "electronic_components": 3,
        "rubber": 2, "polyurethane_foam": 2,
    },

    "Fire Alarm Device": {
        "plastics": 35,
        "electronic_components": 30,
        "printed_wiring_board_mixed_mounted": 20,
        "copper": 10,
        "steel": 5,
    },

    "Heat Interface Unit (HIU)": {
        "steel": 40,
        "copper": 30,
        "brass": 10,
        "plastics": 10,
        "electronic_components": 5,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "Heat pump": {
        "plastics": 4,
        "stainless_steel": 10,
        "aluminium": 7,
        "brass": 1,
        "steel": 60,
        "copper": 10,
        "electronic_components": 3,
    },

    "Lighting Control Device": {
        "plastics": 30,
        "electronic_components": 30,
        "printed_wiring_board_mixed_mounted": 30,
        "copper": 10,
    },

    "Luminaire  LED": {
        "aluminium": 40,
        "steel": 20,
        "plastics": 15,
        "electronic_components": 10,
        "printed_wiring_board_mixed_mounted": 10,
        "glass": 5,
    },

    "MVHR Unit": {
        "steel": 35,
        "aluminium": 15,
        "plastics": 20,
        "copper": 10,
        "insulation": 10,
        "electronic_components": 5,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "Pipe  Copper": {
        "copper": 90,
        "insulation": 10,
    },

    "Pipe  PVC": {
        "pvc": 95,
        "plastics": 5,
    },

    "Pipe  Steel": {
        "steel": 90,
        "insulation": 10,
    },

    "Pipes  PEX": {
        "plastics": 85,
        "pvc": 10,
        "polyethylene": 5,
    },

    "Pump": {
        "cast_iron": 55, "steel": 20, "copper": 10,
        "stainless_steel": 5, "plastics": 5,
        "electronic_components": 3, "rubber": 2,
    },

    "Sensors": {
        "plastics": 30,
        "electronic_components": 35,
        "printed_wiring_board_mixed_mounted": 25,
        "copper": 10,
    },

    "Switchgear": {
        "steel": 45,
        "copper": 25,
        "plastics": 10,
        "stainless_steel": 10,
        "electronic_components": 8,
        "printed_wiring_board_mixed_mounted": 2,
    },

    "Thermal Store": {
        "steel": 70,
        "insulation": 20,
        "plastics": 5,
        "copper": 5,
    },

    "UPS": {
        "steel": 40,
        "copper": 20,
        "electronics": 0,   # unused key
        "electronic_components": 20,
        "plastics": 10,
        "battery_cells": 0, # unused key
        "lithium": 10,
    },
    "Valves": {
        "brass": 60,
        "steel": 20,
        "stainless_steel": 10,
        "rubber": 5,
        "plastics": 5,
    },
    "VAV Box": {
        "steel": 50,
        "aluminium": 20,
        "insulation": 15,
        "electronic_components": 5,
        "plastics": 5,
        "stainless_steel": 3,
        "pvc": 2,
    },

    "VRF Indoor Unit": {
        "steel": 15, "aluminium": 10, "copper": 12,
        "plastics": 30, "insulation": 20,
        "stainless_steel": 3, "electronic_components": 5,
        "pvc": 3, "rubber": 2,
    },

    "VRF Outdoor Unit": {
        "steel": 50, "aluminium": 10, "copper": 20,
        "plastics": 8, "stainless_steel": 4,
        "electronic_components": 4, "printed_wiring_board_mixed_mounted": 3,
        "rubber": 1,
    },
}

# Normalized mapping for case-insensitive lookups (keyed by lower-case product_type)
PRESET_PERCENTAGES_NORMALIZED = {k.lower(): v for k, v in PRESET_PERCENTAGES.items()}



