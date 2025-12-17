from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmbodiedCarbonSerializer
from django.http import HttpResponse
from django.apps import apps
from rest_framework import status
from .data.material_reference import MATERIAL_COEFFS, PRESET_PERCENTAGES
from .data.reference_data import  PRODUCT_LIST,MANUFACTURING_LOCATION,REFRIGERANT_GWP,INSTALLATION_LOCATION
from .calculations.calculations import (calculate_a1_from_instance,calculate_a2_from_instance,calculate_a3_from_instance,calculate_a4_from_instance)
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import getSampleStyleSheet




class EmbodiedCarbonList(APIView):
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


    def get (self, request):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')
        embodied_carbons = EmbodiedCarbon.objects.all()
        serializer = EmbodiedCarbonSerializer(embodied_carbons, many=True)
        return Response(serializer.data)
    
    def post(self, request):    
        data = request.data
        project_name = data.get("project_name")
        product_type = self.get_product(data.get("product_type"))["product"]
        weight_kg = data.get("weight_kg")
        electricity_usage_kwh = data.get("electricity_usage_kwh")
        location_of_factory = self.get_manufacturing_location(data.get("location_of_factory"))["location"]
        lifetime_years = data.get("lifetime_years", None)
        refrigerant_used = self.get_refrigerant(data.get("refrigerant_used"))["refrigerant"]
        refrigerant_charge_kg = data.get("refrigerant_charge_kg", None)
        refrigerant_leakage_rate_pct_per_year = data.get("refrigerant_leakage_rate_pct_per_year", None)
        location_of_use = self.get_installation_location(data.get("location_of_use"))["installation"]


        serializer = EmbodiedCarbonSerializer(data={"project_name": project_name, "product_type": product_type, "weight_kg": weight_kg, "electricity_usage_kwh": electricity_usage_kwh, "location_of_factory": location_of_factory, "lifetime_years": lifetime_years, "refrigerant_used": refrigerant_used, "refrigerant_charge_kg": refrigerant_charge_kg, "refrigerant_leakage_rate_pct_per_year": refrigerant_leakage_rate_pct_per_year, "location_of_use": location_of_use})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.save()
    
        materials_override = data.get("materials_override") or data.get("materials")

        if materials_override and isinstance(materials_override, dict):
            setattr(instance, 'materials_override', materials_override)

        tier = (data.get("freetier") or "basic" or "professional").lower()

        try:
            if tier == 'freetier':
                a1_res = calculate_a1_from_instance(instance)
                a1_val = float(a1_res.get('total_a1', 0.0))
                return Response({ "a1": a1_val,}, status=status.HTTP_201_CREATED)

            if tier == 'basic':
                    a1_val = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    a2_res = calculate_a2_from_instance(instance)
                    a2_val = float(a2_res.get('total_a2', 0.0))

                    a3_res = calculate_a3_from_instance(instance)
                    a3_val = float(a3_res.get('total_a3', 0.0))

                    a4_res = calculate_a4_from_instance(instance)
                    a4_val = float(a4_res.get('total_a4', 0.0))
                    total_a=a1_val + a2_val + a3_val + a4_val
                    return Response({ "a1": a1_val, "a2": a2_val, "a3": a3_val, "a4": a4_val,"total_a": total_a,}, status=status.HTTP_201_CREATED)

            if tier == 'professional':
                    a1_val = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    a2_val = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                    a3_val = float(calculate_a3_from_instance(instance).get('total_a3', 0.0))
                    a4_val = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))

                    return Response({"a1": a1_val,"a2": a2_val,"a3": a3_val,"a4": a4_val,
                    }, status=status.HTTP_201_CREATED)


        except Exception as exc: 
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)



class MaterialsCoefficients(APIView):
    ''' getting materials coefficients '''
    def get(self, request):

        return Response(MATERIAL_COEFFS, status=status.HTTP_200_OK)


class MaterialsPresets(APIView):
    ''' getting and setting preset percentages for materials '''
    def get(self, request):

        return Response(PRESET_PERCENTAGES, status=status.HTTP_200_OK)
    
    def post(self, request):
            product_type = request.data.get("product_type")

            materials = request.data.get("materials", {})

            if not product_type:
                return Response({"error": "product_type is required"}, status=400)
            
            PRESET_PERCENTAGES[product_type] = materials
            
            return Response({"message": "Saved successfully"}, status=200)


class MaterialsElectricityFactors(APIView):
    ''' getting electricity carbon factors for manufacturing locations '''
    def get(self, request):
        try:
            factors = {loc['key']: loc.get('electricity_carbon_factor') for loc in MANUFACTURING_LOCATION}
        except Exception:
            factors = {}
        return Response(factors, status=status.HTTP_200_OK)

class EmbodiedCarbonExportPDF(APIView):
    """Export embodied carbon records as a simple PDF report.

    Optional query params (simple filtering): `product_type`, `location_of_factory`.
    For each record we call `calculate_total_embodied_carbon` to include computed totals.
    """
    def get(self, request):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')

        qs = EmbodiedCarbon.objects.all()
        product_type = request.GET.get('product_type')
        if product_type:
            qs = qs.filter(product_type=product_type)

        location = request.GET.get('location_of_factory')
        if location:
            qs = qs.filter(location_of_factory=location)

        # Build PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
        styles = getSampleStyleSheet()
        elements = []

        # Use provided project name (GET param) if present, otherwise a default title
        project_name = request.GET.get('project_name') or 'Embodied Carbon Report'
        title = Paragraph(project_name, styles['Title'])
        elements.append(title)
        # Show the tier type below the title (GET param `tier`, default 'professional')
        tier = request.GET.get('tier', 'professional')
        tier_display = tier.capitalize() if isinstance(tier, str) else str(tier)
        elements.append(Paragraph(f"Tier: {tier_display}", styles['Normal']))
        elements.append(Spacer(1, 12))

        # Table header
        data = [[
            'ID', 'Product Type', 'Weight (kg)', 'Electricity (kWh)',
            'Factory Location', 'Lifetime (yrs)', 'Refrigerant', 'Refrigerant (kg)',
            'Location of Use', 'Total Embodied Carbon (kgCO2e)'
        ]]

        table = Table(data, repeatRows=1)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d3d3d3')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ]))

        elements.append(table)
        doc.build(elements)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        from django.utils import timezone
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        response['Content-Disposition'] = f'attachment; filename="embodied_carbon_report_{timestamp}.pdf"'
        return response