END_OF_LIFE_PRESETS = {
	# Table entries (product type -> recycle / landfill)
	"heat generation equipment": {"recycle_pct": 70.0, "landfill_pct": 30.0},
	"pipes": {"recycle_pct": 90.0, "landfill_pct": 10.0},
	"ventilation systems": {"recycle_pct": 40.0, "landfill_pct": 60.0},
	"radiator": {"recycle_pct": 80.0, "landfill_pct": 20.0},
	"wire cable": {"recycle_pct": 50.0, "landfill_pct": 50.0},

	# Common generic keys to help lookups from product_type labels used elsewhere
	"ahu": {"recycle_pct": 40.0, "landfill_pct": 60.0},
	"chiller": {"recycle_pct": 40.0, "landfill_pct": 60.0},
	"pipes_generic": {"recycle_pct": 90.0, "landfill_pct": 10.0},
}


def resolve_end_of_life(product_type: str):
	"""Return end-of-life preset for a given product_type string.

	Matching is case-insensitive and will try exact keys, substring matches,
	and simple normalized lookups. Returns a dict with `recycle_pct` and
	`landfill_pct` or None if not found.
	"""
	if not product_type:
		return None

	pt = product_type.strip().lower()

	# direct
	if pt in END_OF_LIFE_PRESETS:
		return END_OF_LIFE_PRESETS[pt]

	# try substring match
	for key in END_OF_LIFE_PRESETS:
		if key in pt or pt in key:
			return END_OF_LIFE_PRESETS[key]

	# fallback: try simple token-based matches
	tokens = pt.split()
	for token in tokens:
		if token in END_OF_LIFE_PRESETS:
			return END_OF_LIFE_PRESETS[token]

	return None

	# Table 2.11 Landfill emission factor (kg CO2e per kg waste)
	# Source: Australian Government Department of Industry, Science, Energy and Resources (2021), Table 49
LANDFILL_EMISSION_FACTOR = 0.2  # kg CO2e / kg waste