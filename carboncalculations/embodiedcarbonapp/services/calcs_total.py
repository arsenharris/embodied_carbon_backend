from .a.calcs_a1 import calculate_a1_from_instance
from .a.calcs_a2 import calculate_a2_from_instance
from .a.calcs_a3 import calculate_a3_from_instance
from .a.calcs_a4 import calculate_a4_from_instance
from .c.calcs_c2 import calculate_c2_from_instance
from .c.calcs_c3 import calculate_c3_from_instance
from .c.calcs_c4 import calculate_c4_from_instance

from typing import Dict, Any  # import typing helpers

def calculate_total_embodied_carbon(instance) -> Dict[str, Any]:
    """
    Calculate the total embodied carbon by summing A1 to C4 stages.
    
    :param instance: EmbodiedCarbon model instance
    :return: Dictionary with total embodied carbon and breakdown
#     """
    a1_result = calculate_a1_from_instance(instance)  # calculate A1 stage
    a2_result = calculate_a2_from_instance(instance)  # calculate A2 stage
    a3_result = calculate_a3_from_instance(instance)  # calculate A3 stage
    a4_result = calculate_a4_from_instance(instance)  # calculate A4 stage   
    c2_result = calculate_c2_from_instance(instance)  # calculate C2 stage   
    c3_result = calculate_c3_from_instance(instance)  # calculate C3 stage   
    c4_result = calculate_c4_from_instance(instance)  # calculate C4 stage   

    total_a1 = float(a1_result.get("total_a1", 0.0))  # extract total A1 value
    total_a2 = float(a2_result.get("a2_kgco2e", 0.0))  # extract total A2 value
    total_a3 = float(a3_result.get("a3_kgco2e", 0.0))  # extract total A3 value
    total_a4 = float(a4_result.get("total_a4_kgco2e", 0.0))  # extract total A4 value

    total_c2 = float(c2_result.get("c2_kgco2e", 0.0))  # extract total C2 value
    total_c3 = float(c3_result.get("c3_kgco2e", 0.0))  # extract total C3 value
    total_c4 = float(c4_result.get("c4_kgco2e", 0.0))  # extract total C4 value


    total_embodied_carbon = total_a1 + total_a2 + total_a3 + total_a4 + total_c2 + total_c3 + total_c4
    return {
        "total_embodied_carbon": total_embodied_carbon,
        "a1_details": a1_result,
        "a2_details": a2_result,
        "a3_details": a3_result,
        "a4_details": a4_result,

        "c2_details": c2_result,
        "c3_details": c3_result,
        "c4_details": c4_result,
    }   
