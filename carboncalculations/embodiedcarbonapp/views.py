from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmbodiedCarbonSerializer
from django.http import HttpResponse
from django.apps import apps
from rest_framework import status
from .data.material_reference import MATERIAL_COEFFS, PRESET_PERCENTAGES
from .data.reference_data import  PRODUCT_LIST,MANUFACTURING_LOCATION,REFRIGERANT_GWP,INSTALLATION_LOCATION
from .calculations.calculations import (calculate_a1_from_instance,calculate_a2_from_instance,calculate_a3_from_instance,calculate_a4_from_instance,calculate_b1andc1_from_instance,calculate_c2_from_instance,calculate_c3_from_instance,calculate_c4_from_instance)
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
        scaleup_factor=1.6
        buffer_factor=1.3

        serializer = EmbodiedCarbonSerializer(data={"project_name": project_name, "product_type": product_type, "weight_kg": weight_kg, "electricity_usage_kwh": electricity_usage_kwh, "location_of_factory": location_of_factory, "lifetime_years": lifetime_years, "refrigerant_used": refrigerant_used, "refrigerant_charge_kg": refrigerant_charge_kg, "refrigerant_leakage_rate_pct_per_year": refrigerant_leakage_rate_pct_per_year, "location_of_use": location_of_use})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.save()
    
        materials_override = data.get("materials_override") or data.get("materials")

        if materials_override and isinstance(materials_override, dict):
            setattr(instance, 'materials_override', materials_override)

        tier = "professional"

        try:
            if tier == 'freetier':
                a1_val_free = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                return Response({ "a1": a1_val_free,}, status=status.HTTP_201_CREATED)

            if tier == 'basic':
                    a1_val = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    a2_val = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                    a3_val = float(calculate_a3_from_instance(instance).get('total_a3', 0.0))
                    a4_val = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))
                    total_a1_replaced=(a1_val)*1.1
                    remaining_life_cycle_stages=total_a1_replaced*scaleup_factor
                    conservative_buffer_factor=remaining_life_cycle_stages*buffer_factor
                    total_b1 = calculate_b1andc1_from_instance(instance).get("total_b1", 0.0)
                    total_c1 = calculate_b1andc1_from_instance(instance).get("total_c1", 0.0)
                    b1_c1_val= total_b1 + total_c1
                    basic_total=conservative_buffer_factor + b1_c1_val

                    return Response({ 
                        "a1": a1_val, 
                        "a2": a2_val, 
                        "a3": a3_val, 
                        "a4": a4_val,
                        "total_a1_a4_replaced": total_a1_replaced, 
                        "remaining life cycle stages":remaining_life_cycle_stages, 
                        "conservative buffer factor": conservative_buffer_factor, 
                        "b1_c1": b1_c1_val,
                        "basic_total": basic_total   
                        }, status=status.HTTP_201_CREATED)
            
            if tier == 'professional':
                    a1_val_pro = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    a2_val_pro = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                    a3_val_pro = float(calculate_a3_from_instance(instance).get('total_a3', 0.0))
                    a4_val_pro = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))
                    total_a1_to_a4_pro=(a1_val_pro+a2_val_pro+a3_val_pro+a4_val_pro)
                    total_c2_pro = calculate_c2_from_instance(instance).get("total_c2", 0.0)
                    total_c3_pro = calculate_c3_from_instance(instance).get("total_c3", 0.0)
                    total_c4_pro = calculate_c4_from_instance(instance).get("total_c4", 0.0)
                    c2_to_c4_pro = total_c2_pro + total_c3_pro + total_c4_pro
                    b3_val_pro = (total_a1_to_a4_pro * 0.1)+(c2_to_c4_pro*0.1)
                    with_buffer_pro=(total_a1_to_a4_pro+c2_to_c4_pro+b3_val_pro)*buffer_factor
                    total_b1_pro = calculate_b1andc1_from_instance(instance).get("total_b1", 0.0)
                    total_c1_pro = calculate_b1andc1_from_instance(instance).get("total_c1", 0.0)
                    b1_c1_val_pro= total_b1_pro + total_c1_pro
                    mid_level=with_buffer_pro + b1_c1_val_pro

                    return Response({
                        "a1": a1_val_pro, 
                        "a2": a2_val_pro, 
                        "a3": a3_val_pro, 
                        "a4": a4_val_pro,
                        "total a1 to a4": total_a1_to_a4_pro, 
                        "total_c2": total_c2_pro,
                        "total_c3": total_c3_pro,
                        "total_c4": total_c4_pro,
                        
                        "c2_to_c4": c2_to_c4_pro,
                        "b3 (10% of a1 to a4)": b3_val_pro,
                        "buffer_factor":with_buffer_pro,
                        "b1": total_b1_pro,
                        "c1": total_c1_pro,
                        "b1_c1": b1_c1_val_pro,
                        "mid level total": mid_level
                    }, status=status.HTTP_201_CREATED)


        except Exception as exc: 
            return Response({"detail": str(exc)}, status=status.HTTP_408_REQUEST_TIMEOUT)



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

        record_id = request.GET.get("id")
        if not record_id:
            return Response({"error": "id is required"}, status=400)


        instance = EmbodiedCarbon.objects.filter(id=record_id).first()
        if not instance:
            return Response({"error": "No data found"}, status=404)

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
        styles = getSampleStyleSheet()
        elements = []

        project_name = request.GET.get('project_name') or 'Embodied Carbon Report'
        elements.append(Paragraph(project_name, styles['Title']))

        tier = request.GET.get('tier', 'professional')
        elements.append(Paragraph(f"Tier: {tier.capitalize()}", styles['Normal']))
        elements.append(Spacer(1, 12))


        # Short lookup: find GWP from REFRIGERANT_GWP and append if found
        refrigerant_display = instance.refrigerant_used or "Not specified"
        normalized = (instance.refrigerant_used or "").strip().lower()
        gwp_val = next((r.get("gwp") for r in REFRIGERANT_GWP if r.get("refrigerant", "").lower() == normalized), None)
        gwp_suffix = f" — GWP: {gwp_val}" if gwp_val is not None else ""
        refrigerant_display = f"{refrigerant_display}{gwp_suffix}"

        data = [
            ["Type of product", instance.product_type],
            ["Capacity", f"{instance.capacity_kw} kW" if instance.capacity_kw else "N/A"],
            ["Product weight", f"{instance.weight_kg} kg" if instance.weight_kg else "N/A"],
            ["Material % breakdown ≥95%", "Yes"],
            ["Product service life", f"{instance.lifetime_years} years" if instance.lifetime_years else "N/A"],
            ["Refrigerant type", refrigerant_display],
            ["Refrigerant charge", f"{instance.refrigerant_charge_kg} kg" if instance.refrigerant_charge_kg else "Not applicable"],
        ]

        table = Table(data, colWidths=[200, 300])
        table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
            ('BACKGROUND', (0, 0), (-1, -1), colors.whitesmoke),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(table)
        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="embodied_carbon_report.pdf"'
        return response