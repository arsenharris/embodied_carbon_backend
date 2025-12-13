END_OF_LIFE_PRESETS = {
	"access control device": {"recycle_pct": 50.0, "landfill_pct": 50},
	"ahu": {"recycle_pct": 40.0, "landfill_pct": 60},
	"boiler": {"recycle_pct": 70.0, "landfill_pct": 30},
	"bms controller": {"recycle_pct": 50.0, "landfill_pct": 50},
	"busbar": {"recycle_pct": 50.0, "landfill_pct": 50},
	"cable containment": {"recycle_pct": 50.0, "landfill_pct": 50},
	"cables": {"recycle_pct": 50.0, "landfill_pct": 50},
	"chiller": {"recycle_pct": 40.0, "landfill_pct": 60},
	"cooling tower": {"recycle_pct": 70.0, "landfill_pct": 30},
	"control panel": {"recycle_pct": 50.0, "landfill_pct": 50},
	"diffuser": {"recycle_pct": 40.0, "landfill_pct": 60},
	"ducted split": {"recycle_pct": 40.0, "landfill_pct": 60},
	"ductwork": {"recycle_pct": 40.0, "landfill_pct": 60},
	"electrical outlet": {"recycle_pct": 50.0, "landfill_pct": 50},
	"fan": {"recycle_pct": 40.0, "landfill_pct": 60},
	"fcu": {"recycle_pct": 40.0, "landfill_pct": 60},
	"fire alarm device": {"recycle_pct": 50.0, "landfill_pct": 50},
	"heat generation equipment": {"recycle_pct": 70.0, "landfill_pct": 30},
	"heat interface unit (hiu)": {"recycle_pct": 70.0, "landfill_pct": 30},
	"heat pump": {"recycle_pct": 70.0, "landfill_pct": 30},
	"lighting control device": {"recycle_pct": 50.0, "landfill_pct": 50},
	"luminaire  led": {"recycle_pct": 50.0, "landfill_pct": 50},
	"mvhr unit": {"recycle_pct": 40.0, "landfill_pct": 60},
	"pipe  copper": {"recycle_pct": 90.0, "landfill_pct": 10},
	"pipe  pvc": {"recycle_pct": 90.0, "landfill_pct": 10},
	"pipe  steel": {"recycle_pct": 90.0, "landfill_pct": 10},
	"pipes": {"recycle_pct": 90.0, "landfill_pct": 10},
	"pipes  pex": {"recycle_pct": 90.0, "landfill_pct": 10},
	"pump": {"recycle_pct": 50.0, "landfill_pct": 50},
	"radiator": {"recycle_pct": 80.0, "landfill_pct": 20},
	"sensors": {"recycle_pct": 50.0, "landfill_pct": 50},
	"switchgear": {"recycle_pct": 50.0, "landfill_pct": 50},
	"thermal store": {"recycle_pct": 70.0, "landfill_pct": 30},
	"ups": {"recycle_pct": 50.0, "landfill_pct": 50},
	"valves": {"recycle_pct": 50.0, "landfill_pct": 50},
	"vav box": {"recycle_pct": 40.0, "landfill_pct": 60},
	"ventilation systems": {"recycle_pct": 40.0, "landfill_pct": 60},
	"vrf indoor unit": {"recycle_pct": 40.0, "landfill_pct": 60},
	"vrf outdoor unit": {"recycle_pct": 40.0, "landfill_pct": 60},
	"wire cable": {"recycle_pct": 50.0, "landfill_pct": 50},
}


PRODUCT_TYPE_TO_COMPLEXITY = {}
for product_type, preset in END_OF_LIFE_PRESETS.items():
    PRODUCT_TYPE_TO_COMPLEXITY[product_type.lower()] = preset["landfill_pct"]

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

	# Table 2.11 Landfill emission factor (kg CO2e per kg waste)
	# Source: Australian Government Department of Industry, Science, Energy and Resources (2021), Table 49
LANDFILL_EMISSION_FACTOR = 0.2  # kg CO2e / kg waste