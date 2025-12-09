# from ..data.materials import , , PRESET_TRANSPORT,TRANSPORT_EMISSION_FACTOR_A2, ELECTRICITY_CARBON_FACTORS, A3_ROUNDS_OF_MANUFACTURING
# from ..models import EmbodiedCarbon
# from typing import Dict, Any  # import typing helpers

# def calculate_a1_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:  # compute A1 using an EmbodiedCarbon model instance
#     """
#     Calculate the A1 embodied carbon based on total weight and material percentages.
    
#     :param total_weight_kg: Total weight of the product in kg
#     :param percentages: Dictionary of material percentages (material_name: percentage)
#     :return: Total A1 embodied carbon in kg CO2e
#     """
#     if instance is None:  # validate instance provided
#         raise ValueError("instance is required")  # raise if no instance

#     product_type = getattr(instance, "product_type", None)  # read product_type from the model instance
#     total_weight_kg = getattr(instance, "weight_kg", None)  # read total weight (kg) from the model instance
#     if product_type is None:  # ensure product_type exists
#         raise ValueError("instance.product_type is required")  # error if missing
#     if total_weight_kg is None:  # ensure weight exists
#         raise ValueError("instance.weight_kg is required")  # error if missing
    
#     preset_percentages = PRESET_PERCENTAGES.get(product_type)  # look up preset percentages for this product type
#     if not preset_percentages:  # ensure preset exists for the product type
#         raise ValueError(f"No preset percentages for product_type '{product_type}'")  # error if missing

#     weights: Dict[str, float] = {}  # will hold computed material weights (kg)
#     a1_components: Dict[str, float] = {}  # will hold computed material embodied carbon (kg CO2e)
#     total_weight_accounted: float = 0.0  # running total of weight accounted by preset percentages
#     total_a1: float = 0.0  # running total of A1 embodied carbon

#     # iterate preset materials and compute each material contribution
#     for material, percentage in preset_percentages.items():  # loop each material and its percentage
#         material_percentage = float(percentage or 0.0)  # ensure percentage is a float
#         material_weight = float(total_weight_kg) * (material_percentage / 100.0)  # compute material weight in kg
#         material_coeff = float(MATERIAL_COEFFS.get(material, MATERIAL_COEFFS.get("steel", 0.0)))  # lookup coefficient (fallback to steel)
#         material_a1 = material_weight * material_coeff  # compute embodied carbon for this material (kgCO2e)

#         weights[material] = material_weight  # store material weight
#         a1_components[material] = material_a1  # store material A1 contribution

#         total_weight_accounted += material_weight  # accumulate accounted weight
#         total_a1 += material_a1  # accumulate total A1

#     remaining_weight = max(0.0, float(total_weight_kg) - total_weight_accounted)  # compute any unaccounted remaining weight
#     if remaining_weight > 0.0:  # if there is remaining weight, assign conservatively to steel
#         remaining_coeff = float(MATERIAL_COEFFS.get("steel", 0.0))  # steel coefficient fallback
#         remaining_a1 = remaining_weight * remaining_coeff  # compute A1 for remaining weight
#         weights["remaining"] = remaining_weight  # store remaining weight
#         a1_components["remaining"] = remaining_a1  # store remaining A1 contribution
#         total_a1 += remaining_a1  # add remaining A1 to total

#     return {  # return structured result
#         "product_type": product_type,  # echo product type used
#         "total_weight_kg": float(total_weight_kg),  # echo total weight
#         "weights": weights,  # per-material weights in kg
#         "a1_components": a1_components,  # per-material embodied carbon in kgCO2e
#         "total_weight_accounted": total_weight_accounted,  # weight accounted by presets
#         "remaining_weight": remaining_weight,  # any remaining weight
#         "total_a1": total_a1,  # total A1 embodied carbon (kgCO2e)
#     }


# def calculate_a2_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
#     """
#     Calculate A2 (transport to site) using the saved model instance:
#       A2 = (weight in tonnes) * distance_km * emission_factor (kgCO2e / t·km)
#     Returns a dict with distance_km, weight_tonnes and a2_kgco2e
#     """
#     if instance is None:
#         raise ValueError("instance is required")

#     product_type = getattr(instance, "product_type", None)  # get product type from model
#     weight_kg = getattr(instance, "weight_kg", None)        # get weight (kg) from model
#     if product_type is None:
#         raise ValueError("instance.product_type is required")
#     if weight_kg is None:
#         raise ValueError("instance.weight_kg is required")

#     transport_preset = PRESET_TRANSPORT.get(product_type)
#     if not transport_preset:
#         # no preset: user must supply distance externally — raise for now
#         raise ValueError(f"No transport preset for product_type '{product_type}'")

#     distance_km = float(transport_preset.get("a2_distance_km", 0.0))  # km to transport
#     weight_tonnes = float(weight_kg) / 1000.0                         # convert kg -> t
#     emission_factor = float(TRANSPORT_EMISSION_FACTOR_A2)            # kgCO2e / t·km

#     a2_kgco2e = weight_tonnes * distance_km * emission_factor        # compute A2

#     return {
#         "product_type": product_type,
#         "distance_km": distance_km,
#         "weight_tonnes": weight_tonnes,
#         "emission_factor_kg_per_t_km": emission_factor,
#         "a2_kgco2e": a2_kgco2e,
#     }   


# def calculate_a3_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
#     """
#     Calculate A3 (manufacturing energy) using the saved model instance and presets.
#     A3 = energy_kwh_per_unit * rounds_of_manufacture * electricity_carbon_factor (kgCO2e)
#     Returns a dict with energy_kwh_per_unit, rounds_of_manufacture, carbon_factor and a3_kgco2e.
#     """
#     if instance is None:
#         raise ValueError("instance is required")

#     product_type = getattr(instance, "product_type", None)  # read product type from model
#     if product_type is None:
#         raise ValueError("instance.product_type is required")

#     manufacture_preset = PRESET_MANUFACTURE.get(product_type)
#     if not manufacture_preset:
#         raise ValueError(f"No manufacturing preset for product_type '{product_type}'")

#     energy_kwh_per_unit = float(manufacture_preset.get("energy_kwh_per_unit", 0.0))  # kW·h per unit
#     rounds_of_manufacture = float(manufacture_preset.get("rounds_of_manufacture", 1.0))  # rounds count
#     region = manufacture_preset.get("manufacture_region", None)  # manufacturing region key

#     carbon_factor = float(ELECTRICITY_CARBON_FACTORS.get(region, ELECTRICITY_CARBON_FACTORS.get("China", 0.54)))  # kgCO2e / kW·h

#     a3_kgco2e = energy_kwh_per_unit * rounds_of_manufacture * carbon_factor  # compute A3

#     return {
#         "product_type": product_type,
#         "energy_kwh_per_unit": energy_kwh_per_unit,
#         "rounds_of_manufacture": rounds_of_manufacture,
#         "manufacture_region": region,
#         "electricity_carbon_factor_kg_per_kwh": carbon_factor,
#         "a3_kgco2e": a3_kgco2e,
#     }


# def calculate_a4_from_instance(instance: EmbodiedCarbon) -> Dict[str, Any]:
#     """
#     Calculate A4 (transport to site) using the saved model instance and presets.
#     A4 = weight_tonnes * (sea_distance_km * ship_factor + road_distance_km * hgv_factor)
#     Returns a dict with distances, factors and a4_kgco2e.
#     """
#     if instance is None:
#         raise ValueError("instance is required")

#     product_type = getattr(instance, "product_type", None)  # read product type from model
#     weight_kg = getattr(instance, "weight_kg", None)        # read product weight from model
#     if product_type is None:
#         raise ValueError("instance.product_type is required")
#     if weight_kg is None:
#         raise ValueError("instance.weight_kg is required")

#     a4_preset = PRESET_A4.get(product_type)
#     if not a4_preset:
#         raise ValueError(f"No A4 preset for product_type '{product_type}'")

#     sea_distance_km = float(a4_preset.get("sea_distance_km", 0.0))   # sea leg km
#     road_distance_km = float(a4_preset.get("road_distance_km", 0.0)) # road leg km

#     weight_tonnes = float(weight_kg) / 1000.0                         # convert kg -> t

#     ship_factor = float(SHIP_EMISSION_FACTOR)                         # kgCO2e / t·km for sea
#     hgv_factor = float(TRANSPORT_EMISSION_FACTOR_A2)                  # kgCO2e / t·km for road (HGV)

#     a4_kgco2e = weight_tonnes * (sea_distance_km * ship_factor + road_distance_km * hgv_factor)  # compute A4

#     return {
#         "product_type": product_type,
#         "weight_tonnes": weight_tonnes,
#         "sea_distance_km": sea_distance_km,
#         "road_distance_km": road_distance_km,
#         "ship_emission_factor_kg_per_t_km": ship_factor,
#         "road_emission_factor_kg_per_t_km": hgv_factor,
#         "a4_kgco2e": a4_kgco2e,
#     }