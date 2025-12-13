from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmbodiedCarbonSerializer
from .data.a.materials_a1 import MATERIAL_COEFFS, PRESET_PERCENTAGES
from .data.a.materials_a3 import ELECTRICITY_CARBON_FACTORS
from django.apps import apps
from rest_framework import status
from .services.calcs_total import calculate_total_embodied_carbon

class EmbodiedCarbonList(APIView):
    def get (self, request):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')
        embodied_carbons = EmbodiedCarbon.objects.all()
        serializer = EmbodiedCarbonSerializer(embodied_carbons, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Accept request payload with at least 'product_type' and 'weight_kg'.
        # The view will save the minimal model and then run the calculation service
        # which reads the values from the saved model instance.        
        data = request.data
        product_type = data.get("product_type")
        weight_kg = data.get("weight_kg")
        electricity_usage_kwh = data.get("electricity_usage_kwh")
        location_of_factory = data.get("location_of_factory")
        # Use serializer to validate and persist minimal model (product_type + weight_kg)
        serializer = EmbodiedCarbonSerializer(data={"product_type": product_type, "weight_kg": weight_kg, "electricity_usage_kwh": electricity_usage_kwh, "location_of_factory": location_of_factory})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        instance = serializer.save()

        # If frontend provided a materials override in the request payload, attach
        # it to the instance so calculation services can use it for this run.
        materials_override = data.get("materials_override") or data.get("materials")
        if materials_override and isinstance(materials_override, dict):
            # attach as a temporary attribute (not persisted) used by calculation
            setattr(instance, 'materials_override', materials_override)

        # Run the calculation based on the saved model instance (service reads presets)
        try:
            calculation_total = calculate_total_embodied_carbon(instance)  # compute full lifecycle totals
        except Exception as exc:  # if calculation fails
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)  # return error response

        # Build simplified result format: a1, a2, a3, a4 and a1_to_a4_total
        a1_val = calculation_total.get("a1_details", {}).get("a1_kgco2e", 0.0)
        a2_val = calculation_total.get("a2_details", {}).get("a2_kgco2e", 0.0)
        a3_val = calculation_total.get("a3_details", {}).get("a3_kgco2e", 0.0)
        a4_val = calculation_total.get("a4_details", {}).get("a4_kgco2e", 0.0)
        a1_to_a4_total = a1_val + a2_val + a3_val + a4_val
        c2_val = calculation_total.get("c2_details", {}).get("c2_kgco2e", 0.0)
        c3_val = calculation_total.get("c3_details", {}).get("c3_kgco2e", 0.0)
        c4_val = calculation_total.get("c4_details", {}).get("c4_kgco2e", 0.0)
        c2_to_c4_total = c2_val + c3_val + c4_val   
        return Response({
            "a1": a1_val,
            "a2": a2_val,
            "a3": a3_val,
            "a4": a4_val,
            "a1_to_a4_total": a1_to_a4_total,
            "c2": c2_val,
            "c3": c3_val,
            "c4": c4_val,
            "c2_to_c4_total": c2_to_c4_total,
            "total_embodied_carbon": calculation_total.get("total_embodied_carbon", 0.0),
        }, status=status.HTTP_201_CREATED)


class MaterialsCoefficients(APIView):
    """Return the embodied carbon coefficients (MATERIAL_COEFFS) for materials.

    This endpoint exposes the values defined in `data/a/materials_a1.py` so the
    frontend MaterialEditor can fetch them.
    """
    def get(self, request):
        return Response(MATERIAL_COEFFS, status=status.HTTP_200_OK)


class MaterialsPresets(APIView):
    """Return preset percentage allocations for products (from materials_a1.PRESET_PERCENTAGES).

    Frontend will request this endpoint to obtain per-product allocations (e.g. "AHU").
    """
    def get(self, request):
        return Response(PRESET_PERCENTAGES, status=status.HTTP_200_OK)
    def post(self, request):
            product_type = request.data.get("product_type")
            materials = request.data.get("materials", {})

            if not product_type:
                return Response({"error": "product_type is required"}, status=400)

            # Save/update here
            PRESET_PERCENTAGES[product_type] = materials

            return Response({"message": "Saved successfully"}, status=200)


class MaterialsElectricityFactors(APIView):
    """Return electricity carbon factors (ELECTRICITY_CARBON_FACTORS) for A3.

    Frontend should call this to populate a dropdown so users can choose the
    manufacturing electricity carbon factor (location key).
    """
    def get(self, request):
        return Response(ELECTRICITY_CARBON_FACTORS, status=status.HTTP_200_OK)