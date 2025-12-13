REFRIGERANT_LEAKAGE_SCENARIOS = [
	{
		"product_type": "Charge greater than 100 kg (type A)",
		"annual_leakage_rate_b1_use": 0.09,
		"end_of_life_leakage_rate_c1_deconstruction": 0.05,
	},
	{
		"product_type": "Charge less than 100 kg (type B)",
		"annual_leakage_rate_b1_use": 0.09,
		"end_of_life_leakage_rate_c1_deconstruction": 0.30,
	},
]

# Table 2.2 - Global warming potential (GWP) of refrigerants
# Values marked "<1" in the source are stored here as 0.25 (numeric) to
# make them usable in calculations while keeping them below 1. If you prefer
# a different representative value (e.g. 0.0 or 1.0) change the entries below.
REFRIGERANT_GWP = [
	{"refrigerant": "R11", "gwp_100yr": 4660.0},
	{"refrigerant": "R22", "gwp_100yr": 1760.0},
	{"refrigerant": "R470c", "gwp_100yr": 1624.21},
	{"refrigerant": "R410a", "gwp_100yr": 1923.5},
	{"refrigerant": "R134a", "gwp_100yr": 1300.0},
	{"refrigerant": "R32", "gwp_100yr": 677.0},
	{"refrigerant": "R1234yf", "gwp_100yr": 0.25},
	{"refrigerant": "R1234ze", "gwp_100yr": 0.25},
	{"refrigerant": "R290", "gwp_100yr": 3.0},
	{"refrigerant": "R744", "gwp_100yr": 1.0},
	{"refrigerant": "R717", "gwp_100yr": 0.0},
	{"refrigerant": "R718", "gwp_100yr": 0.0},
]

