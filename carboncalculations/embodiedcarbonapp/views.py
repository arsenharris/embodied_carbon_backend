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

        # Run the calculation based on the saved model instance (service reads presets)
        try:
            calculation_total = calculate_total_embodied_carbon(instance)  # compute full lifecycle totals
        except Exception as exc:  # if calculation fails
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)  # return error response

        return Response({  # return created instance info plus calculation result
            "id": instance.id,  # saved record id
            "product_type": instance.product_type,  # echo product type
            "weight_kg": instance.weight_kg,  # echo weight
            "electricity_usage_kwh": instance.electricity_usage_kwh,  # echo electricity usage
            "location_of_factory": instance.location_of_factory,  # echo factory location
            "calculation_total": calculation_total,  # full lifecycle calculation dict
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