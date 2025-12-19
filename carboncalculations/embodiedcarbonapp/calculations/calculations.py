from ..data.material_reference import MATERIAL_COEFFS, PRESET_PERCENTAGES, PRESET_PERCENTAGES_NORMALIZED,TRANSPORT_EMISSION_FACTOR_A2_C2,TRANSPORT_EMISSION_FACTORS_SEA,LANDFILL_EMISSION_FACTOR,REFRIGERANT_LEAKAGE_SCENARIOS
from ..data.reference_data import PRODUCT_LIST,MANUFACTURING_LOCATION,REFRIGERANT_GWP,INSTALLATION_LOCATION
from ..models import EmbodiedCarbon
from typing import Dict, Any 

def get_product(self, product_type: str) -> dict:
        normalized = product_type.strip().lower()
        for product in PRODUCT_LIST:
            if product["product"].lower() == normalized or product.get("display_name", "").lower() == normalized:
                return product
        raise ValueError(f"Invalid product_type '{product_type}'")
def get_manufacturing_location(self,location_of_factory: str) -> dict:
    normalized = location_of_factory.strip().lower()
    for location in MANUFACTURING_LOCATION:
        if location["location"] .lower()== normalized or location.get("display_name", "").lower() == normalized:
            return location
    raise ValueError(f"Invalid location_of_factory '{self,location_of_factory}'")
    
def get_installation_location(self, location_of_use: str) -> dict:
    normalized = location_of_use.strip().lower()
    for install in INSTALLATION_LOCATION:
        if install["installation"] .lower() == normalized or install.get("display_name", "").lower() == normalized:
            return install
    raise ValueError(f"Invalid location_of_use '{location_of_use}'")

def get_refrigerant(self,refrigerant_used: str) -> dict:
    normalized = refrigerant_used.strip().lower()
    for ref in REFRIGERANT_GWP:
        if ref["refrigerant"].lower() == normalized or ref.get("display_name", "").lower() == normalized:
            return ref
    raise ValueError(f"Invalid refrigerant '{refrigerant_used}'")

def calculate_a1_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]: 

    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
    if total_weight_kg is None:  # ensure weight exists
        raise ValueError("instance.weight_kg is required")  # error if missing
    
    preset_percentages = getattr(instance, 'materials_override', None)
    # Try exact lookup first, then fallback to case-insensitive mapping from built-in presets.
    # PRESET_PERCENTAGES keys sometimes use spaces while product_type values use underscores
    # (e.g. "access control device" vs "access_control_device"). Try a few normalized variants.
    if not preset_percentages:
        lookup_key = (product_type or "").strip().lower()
        # exact match against original presets
        preset_percentages = PRESET_PERCENTAGES.get(lookup_key)
    if not preset_percentages:
        # keys in PRESET_PERCENTAGES_NORMALIZED are lowercased versions of the preset keys
        preset_percentages = PRESET_PERCENTAGES_NORMALIZED.get(lookup_key)
    if not preset_percentages:
        # try replacing underscores with spaces (common mismatch between PRODUCT_LIST and PRESET keys)
        preset_percentages = PRESET_PERCENTAGES_NORMALIZED.get(lookup_key.replace("_", " "))
    if not preset_percentages:
        # as a last fallback, try replacing spaces with underscores (in case some presets use underscores)
        preset_percentages = PRESET_PERCENTAGES_NORMALIZED.get(lookup_key.replace(" ", "_"))
    if not preset_percentages:
        raise ValueError(f"No preset percentages for product_type '{product_type}'")  # error if missing

    weights: Dict[str, float] = {}  # will hold computed material weights (kg)
    a1_components: Dict[str, float] = {}  # will hold computed material embodied carbon (kg CO2e)
    total_weight_accounted: float = 0.0  # running total of weight accounted by preset percentages
    total_a1: float = 0.0  # running total of A1 embodied carbon

    # iterate preset materials and compute each material contribution
    for material, percentage in preset_percentages.items():  # loop each material and its percentage
        material_percentage = float(percentage or 0.0)  # ensure percentage is a float
        material_weight = float(total_weight_kg) * (material_percentage / 100.0)  # compute material weight in kg
        material_coeff = float(MATERIAL_COEFFS.get(material, MATERIAL_COEFFS.get("steel", 0.0)))  # lookup coefficient (fallback to steel)
        material_a1 = material_weight * material_coeff  # compute embodied carbon for this material (kgCO2e)
        weights[material] = material_weight  # store material weight
        a1_components[material] = material_a1  # store material A1 contribution
        total_weight_accounted += material_weight  # accumulate accounted weight
        total_a1 += material_a1  # accumulate total A1

    remaining_weight = max(0.0, float(total_weight_kg) - total_weight_accounted)  # compute any unaccounted remaining weight
    if remaining_weight > 0.0:
        # Attribute any small remaining mass to `steel` (merge with existing steel entry)
        steel_coeff = float(MATERIAL_COEFFS.get("steel", 0.0))
        remaining_a1 = remaining_weight * steel_coeff
        weights["steel"] = weights.get("steel", 0.0) + remaining_weight
        a1_components["steel"] = a1_components.get("steel", 0.0) + remaining_a1
        total_a1 += remaining_a1
    return {  # return structured result
        "total_a1": total_a1,  # total A1 embodied carbon (kgCO2e)
    }

def calculate_a2_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
    if total_weight_kg is None:  # ensure weight exists
        raise ValueError("instance.weight_kg is required")  # error if missing
    weight_tonnes = float(total_weight_kg) / 1000.0                         # convert kg -> t
    emission_factor = float(TRANSPORT_EMISSION_FACTOR_A2_C2)            # kgCO2e / t·km

    for product in PRODUCT_LIST:
        if product["product"].lower() == product_type.lower():
            a2_distance_km = product["a2_distance_km"]
            break
    else:
        raise ValueError(f"No product found for product_type '{product_type}'")
    total_a2 = weight_tonnes * a2_distance_km * emission_factor        # compute A2
    return {
        "total_a2": total_a2,
    }  

def calculate_a3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    energy_kwh_per_unit = getattr(instance, "electricity_usage_kwh", None)
    if energy_kwh_per_unit is None:  # ensure energy usage exists
        raise ValueError("instance.electricity_usage_kwh is required")  # error if missing


    location_of_factory = getattr(instance, "location_of_factory", None)
    if location_of_factory is None:  # ensure location exists
        raise ValueError("instance.location_of_factory is required")  # error if missing
    
    for product in PRODUCT_LIST:
        if product["product"].lower() == product_type.lower():
            a3_rounds_of_manufacture = product["a3_rounds_of_manufacture"]
            break
    else:
        raise ValueError(f"No product found for product_type '{product_type}'")
    
    for location in MANUFACTURING_LOCATION:
        if location["location"].lower() == location_of_factory.lower():
            electricity_carbon_factor = location["electricity_carbon_factor"]
            break
    else:
        raise ValueError(f"No electricity carbon factor found for location_of_factory '{location_of_factory}'")

    total_a3 = energy_kwh_per_unit * a3_rounds_of_manufacture * electricity_carbon_factor
    
    return {
        "total_a3": total_a3,
    }

def calculate_a4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
    if total_weight_kg is None:  # ensure weight exists
        raise ValueError("instance.weight_kg is required")  # error if missing
    weight_tonnes = float(total_weight_kg) / 1000.0                         # convert kg -> t

    location_of_use = getattr(instance, "location_of_use", None)
    if location_of_use is None:  # ensure location exists
        raise ValueError("instance.location_of_use is required")  # error if missing

    for distance in INSTALLATION_LOCATION:
        if distance["installation"].lower() == location_of_use.lower():
            road_km = distance["road_km"]
            sea_km = distance["sea_km"]
            break
    else:
        raise ValueError(f"No product found for product_type '{product_type}'")
    
    total_a4= weight_tonnes * (road_km*TRANSPORT_EMISSION_FACTOR_A2_C2 + sea_km*TRANSPORT_EMISSION_FACTORS_SEA)

    return {
        "total_a4": total_a4,
    }

def calculate_b1andc1_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance
    
    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    refrigerant_used = getattr(instance, "refrigerant_used", None)
    if refrigerant_used is None:
        raise ValueError("instance.refrigerant_used is required")

    refrigerant_charge_kg = getattr(instance, "refrigerant_charge_kg", None)
    if refrigerant_charge_kg is None:
        raise ValueError("instance.refrigerant_charge_kg is required")
    
    lifetime_years = getattr(instance, "lifetime_years", None)
    if lifetime_years is None:
        raise ValueError("instance.lifetime_years is required")
    
    for refrigerant in REFRIGERANT_GWP:
        if refrigerant["refrigerant"].lower() == refrigerant_used.lower():
            gwp = refrigerant["gwp"]
            break
    else:
        raise ValueError(f"No product found for refrigerant '{refrigerant_used}'")

    if refrigerant_charge_kg >= 100:
        scenario_index = 0  # first scenario: charge >=100 kg

    else:
        scenario_index = 1  # second scenario: charge <100 kg

    annual_leakage_rate_b1_use = REFRIGERANT_LEAKAGE_SCENARIOS[scenario_index]["annual_leakage_rate_b1_use"]
    end_of_life_leakage_rate_c1_deconstruction = REFRIGERANT_LEAKAGE_SCENARIOS[scenario_index]["end_of_life_leakage_rate_c1_deconstruction"]

    total_b1 = refrigerant_charge_kg * annual_leakage_rate_b1_use * gwp *lifetime_years

    # C1: end-of-life leakage applied once at deconstruction
    total_c1 = refrigerant_charge_kg * end_of_life_leakage_rate_c1_deconstruction * gwp
    totalb1_c1= total_b1 + total_c1
    return {
        "annual_leakage_rate_b1_use": annual_leakage_rate_b1_use,
        "end_of_life_leakage_rate_c1_deconstruction": end_of_life_leakage_rate_c1_deconstruction,
        "total_b1": total_b1,
        "total_c1": total_c1,
        "total b1 and c1": totalb1_c1,
    }

def calculate_c2_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:

    if instance is None:
        raise ValueError("instance is required")

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
    if total_weight_kg is None:  # ensure weight exists
        raise ValueError("instance.weight_kg is required")  # error if missing
    weight_tonnes = float(total_weight_kg) / 1000.0    

    for product in PRODUCT_LIST:
        if product["product"].lower() == product_type.lower():
            c2_distance_km = product["c2_distance_km"]
            break
    else:
        raise ValueError(f"No product found for product_type '{product_type}'")
    
    total_c2 = weight_tonnes * c2_distance_km * TRANSPORT_EMISSION_FACTOR_A2_C2  
    return {
        "total_c2": total_c2,
    }

def calculate_c3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    location_of_factory = getattr(instance, "location_of_factory", None)
    if location_of_factory is None:  # ensure location exists
        raise ValueError("instance.location_of_factory is required")  # error if missing
    energy_kwh_per_unit = getattr(instance, "electricity_usage_kwh", None)

    for location in MANUFACTURING_LOCATION:
        if location["location"].lower() == location_of_factory.lower():
            electricity_carbon_factor = location["electricity_carbon_factor"]
            break
    else:
        raise ValueError(f"No product found for product_type '{location_of_factory}'")
    total_c3 = energy_kwh_per_unit * electricity_carbon_factor
    return {
        "total_c3": total_c3,
    }

def calculate_c4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
    
    if instance is None:  # validate instance provided
        raise ValueError("instance is required")  # raise if no instance

    product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
    if product_type is None:  # ensure product_type exists
        raise ValueError("instance.product_type is required")  # error if missing
    
    total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
    for product in PRODUCT_LIST:
        if product["product"].lower() == product_type.lower():
            landfill_pct = product["landfill_pct"]
            break
    else:
        raise ValueError(f"No product found for product_type '{product_type}'")
    total_c4 = float(total_weight_kg)* landfill_pct * LANDFILL_EMISSION_FACTOR
    return {
        "total_c4": total_c4,
    }
