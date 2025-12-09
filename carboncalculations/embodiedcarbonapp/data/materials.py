# #####Basic Calculation assumptions for embodied carbon calculations#####

# ### Table 2.1 TM 65 - Refrigerant leakage scenarios###
# # B1: annual leakage rates (used during use phase)
# B1_LEAKAGE_RATES = {
#     "charge_greater_than_100kg": 0.09,
#     "charge_less_or_equal_100kg": 0.09,
# }

# C1_LEAKAGE_RATES = {
#     "charge_greater_than_100kg": 0.05,
#     "charge_less_or_equal_100kg": 0.30,
# }

# ### Table 2.2 TM 65 - Global warming potential of refrigerants###
# # Notes:Table 2.2 in TM65 (CIBSE, 2021a), about refrigerant global warming potential, is superseded by Table 2.2 below when using the methodology in Australia and New Zealand.
# # Global Warming Potential (GWP) for refrigerants (100-year time horizon, kg CO2e per kg)
# # Values taken from IPCC / common published figures. Use conservative numeric values.
# REFRIGERANT_GWP = {
#     "R11": 4660.0,
#     "R22": 1760.0,
#     "R470c": 1624.21,
#     "R410a": 1923.5,
#     "R134a": 1300.0,
#     "R32": 677.0,
#     "R1234yf": 1.0,   # "<1" recorded in table — use 1.0 conservatively
#     "R1234ze": 1.0,   # "<1" recorded in table — use 1.0 conservatively
#     "R290": 3.0,
#     "R744": 1.0,
#     "R717": 0.0,
#     "R718": 0.0,
# }






# PRODUCT_TYPE_TO_COMPLEXITY = {
#     "Heat pump": "category_3_high_complexity",   # map Heat pump -> high complexity
#     "Chiller": "category_3_high_complexity",     # map Chiller -> high complexity
#     "Ducted split": "category_3_high_complexity",
#     "Pump": "category_2_medium_complexity",
#     "Pumps": "category_2_medium_complexity",
#     "Luminaires": "category_2_medium_complexity",
#     "Sensor": "category_2_medium_complexity",
#     # add more explicit mappings as needed
# }



# #Table 2.7 Carbon factors for gas: A3 (manufacturing) (supersedes Table 4.11 in TM65)

# GAS_CARBON_FACTORS = {
#     "natural_gas": {
#         "kgco2e_per_gj": 59.52,     # kg CO2e per gigajoule (GJ)
#         "kgco2e_per_kwh": 0.214,    # kg CO2e per kilowatt-hour (kW·h)
#     },
# }





# # Table 2.9 Refrigerant leakage scenarios: B1 (use), C1 (deconstruction) (supersedes Table 4.13 in TM65)

# B1_LEAKAGE_RATES = {
#     "type_A_charge_gt_100kg": 0.09,   # annual leakage rate for charge > 100 kg (B1)
#     "type_B_charge_le_100kg": 0.09,   # annual leakage rate for charge ≤ 100 kg (B1)
# }

# C1_LEAKAGE_RATES = {
#     "type_A_charge_gt_100kg": 0.05,   # end-of-life leakage fraction for charge > 100 kg (C1)
#     "type_B_charge_le_100kg": 0.30,   # end-of-life leakage fraction for charge ≤ 100 kg (C1)
# }

# #Table 2.10 Recycling rate at end of life: C3 (waste processing), C4 (disposal) (Table 4.14 in TM65)
# RECYCLING_RATES_C3_C4 = {
#     "Heat generation equipment": {"recycle_percentage": 70, "landfill_percentage": 30},
#     "Pipes": {"recycle_percentage": 90, "landfill_percentage": 10},
#     "Ventilation systems": {"recycle_percentage": 40, "landfill_percentage": 60},
#     "Radiator": {"recycle_percentage": 80, "landfill_percentage": 20},
#     "Wire cable": {"recycle_percentage": 50, "landfill_percentage": 50},
# }


# # Table 2.11 Landfill emission: C4 (disposal) (supersedes Table 4.15 in TM65)
# LANDFILL_EMISSION_C4 = {
#     "all_building_services_equipment": 0.2,  # kgCO2e per kg waste
# }
# # 


