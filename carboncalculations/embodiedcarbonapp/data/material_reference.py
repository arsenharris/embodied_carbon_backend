
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
    "ahu": {
        "steel": 45, 
        "aluminium": 15, 
        "copper": 10,
        "plastics": 8, 
        "insulation": 12,
        "stainless_steel": 3, 
        "electronic_components": 2,
        "pvc": 2, "rubber": 2, 
        "polyurethane_foam": 1,
    },

    "access control device": {
        "plastics": 50,
        "electronic_components": 30,
        "printed_wiring_board_mixed_mounted": 10,
        "stainless_steel": 5,
    },

    "bms Controller": {
        "plastics": 20,
        "electronic_components": 35,
        "printed_wiring_board_mixed_mounted": 35,
        "copper": 10,
    },

    "boiler": {
        "steel": 60, 
        "cast_iron": 20,
        "copper": 5, 
        "stainless_steel": 5,
        "plastics": 3, 
        "rubber": 2,
        "electronic_components": 3,
        "pvc": 2,
    },

    "busbar": {
        "copper": 70,
        "steel": 20,
        "plastics": 10,
    },

    "cable containment": {
        "steel": 85,
        "aluminium": 10,
        "zinc": 5,
    },

    "cables": {
        "copper": 55,
        "pvc": 35,
        "plastics": 10,
    },

    "chiller": {
        "steel": 65,
        "aluminium": 15, 
        "copper": 5, 
        "plastics": 3,
        "stainless_steel": 2, 
        "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, 
    },

    "control panel": {
        "steel": 50,
        "copper": 20,
        "plastics": 10,
        "electronic_components": 15,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "Cooling Tower": {
        "plastics": 40,
        "copper": 5,
        "stainless_steel": 20,
        "rubber": 5,
        "electronic_components": 3,
        "polyurethane_foam": 3,
        "polypropylene": 20,
    },

    "ducted split": {
        "steel": 40, 
        "aluminium": 15, 
        "copper": 8, 
        "plastics": 22,
        "stainless_steel": 7, 
        "electronic_components": 3,
        "printed_wiring_board_mixed_mounted": 2, 
    },

    "ductwork": {
        "steel": 80,
        "insulation": 12,
        "pvc": 3,
        "rubber": 2,
        "polyurethane_foam": 3,
    },

    "diffuser": {
        "aluminium": 75,
        "steel": 15,
        "plastics": 5,
    },

    "electrical outlet": {
        "plastics": 40,
        "copper": 30,
        "steel": 15,
        "electronic_components": 10,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "fan": {
        "steel": 55,
        "aluminium": 10,
        "copper": 20,
        "plastics": 10,
        "stainless_steel": 3,
        "electronic_components": 2,
    },

    "fcu": {
        "steel": 40,
        "aluminium": 10, 
        "copper": 20,
        "plastics": 10, 
        "insulation": 10,
        "electronic_components": 3,
        "polyurethane_foam": 2,
    },

    "fire alarm device": {
        "plastics": 35,
        "electronic_components": 30,
        "printed_wiring_board_mixed_mounted": 20,
        "copper": 10,
        "steel": 5,
    },

    "heat interface unit": {
        "steel": 40,
        "copper": 30,
        "brass": 10,
        "plastics": 10,
        "electronic_components": 5,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "heat pump": {
        "plastics": 4,
        "stainless_steel": 10,
        "aluminium": 7,
        "brass": 1,
        "steel": 60,
        "copper": 10,
        "electronic_components": 3,
    },

    "lighting control device": {
        "plastics": 30,
        "electronic_components": 30,
        "printed_wiring_board_mixed_mounted": 30,
        "copper": 10,
    },

    "luminaire_led": {
        "aluminium": 40,
        "steel": 20,
        "plastics": 15,
        "electronic_components": 10,
        "printed_wiring_board_mixed_mounted": 10,
        "glass": 5,
    },

    "mvhr_unit": {
        "steel": 35,
        "aluminium": 15,
        "plastics": 20,
        "copper": 10,
        "insulation": 10,
        "electronic_components": 5,
        "printed_wiring_board_mixed_mounted": 5,
    },

    "pipe": {
        "copper": 90,
        "insulation": 10,
    },

    "pump": {
        "cast_iron": 55, 
        "steel": 20, 
        "copper": 10,
        "stainless_steel": 5, 
        "plastics": 5,
        "electronic_components": 3, 
        "rubber": 2,
    },

    "sensors": {
        "plastics": 30,
        "electronic_components": 35,
        "printed_wiring_board_mixed_mounted": 25,
        "copper": 10,
    },

    "switchgear": {
        "steel": 45,
        "copper": 25,
        "plastics": 10,
        "stainless_steel": 10,
        "electronic_components": 8,
        "printed_wiring_board_mixed_mounted": 2,
    },

    "thermal_store": {
        "steel": 70,
        "insulation": 20,
        "plastics": 5,
        "copper": 5,
    },

    "ups": {
        "steel": 40,
        "copper": 20,
        "electronic_components": 20,
        "plastics": 10,
        "lithium": 10,
    },
    "valves": {
        "brass": 60,
        "steel": 20,
        "stainless_steel": 10,
        "rubber": 5,
        "plastics": 5,
    },
    "vav_box": {
        "steel": 50,
        "aluminium": 20,
        "insulation": 15,
        "electronic_components": 5,
        "plastics": 5,
        "stainless_steel": 3,
        "pvc": 2,
    },

    "vrf_indoor_unit": {
        "steel": 15, 
        "aluminium": 10, 
        "copper": 12,
        "plastics": 30, 
        "insulation": 20,
        "stainless_steel": 3, 
        "electronic_components": 5,
        "pvc": 3, 
        "rubber": 2,
    },

    "vrf_outdoor_unit": {
        "steel": 50, 
        "aluminium": 10, 
        "copper": 20,
        "plastics": 8, 
        "stainless_steel": 2,
        "electronic_components": 6, 
        "printed_wiring_board_mixed_mounted": 3,
        "rubber": 1,
    },
}

PRESET_PERCENTAGES_NORMALIZED = {k.lower(): v for k, v in PRESET_PERCENTAGES.items()}
TRANSPORT_EMISSION_FACTOR_A2_C2 = 0.133  # kgCO2e / t·km (BEIS average HGV)
TRANSPORT_EMISSION_FACTORS_SEA = 0.02
LANDFILL_EMISSION_FACTOR = 0.2  # kg CO2e / kg waste
REFRIGERANT_LEAKAGE_SCENARIOS = [
	{
		# "product_type": "Capacity greater than 100 kg (type A)",
		"annual_leakage_rate_b1_use": 0.09,
		"end_of_life_leakage_rate_c1_deconstruction": 0.05,
	},
	{
		# "product_type": "Capacity less than 100 kg (type B)",
		"annual_leakage_rate_b1_use": 0.09,
		"end_of_life_leakage_rate_c1_deconstruction": 0.30,
	},
]
