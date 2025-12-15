from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmbodiedCarbonSerializer
from .data.a.materials_a1 import MATERIAL_COEFFS, PRESET_PERCENTAGES
from .data.a.materials_a3 import ELECTRICITY_CARBON_FACTORS
from django.apps import apps
from rest_framework import status
from .services.calcs_total import calculate_total_embodied_carbon
from django.http import HttpResponse
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import getSampleStyleSheet

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
        lifetime_years = data.get("lifetime_years", None)
        refrigerant_used = data.get("refrigerant_used", None)
        refrigerant_charge_kg = data.get("refrigerant_charge_kg", None)
        refrigerant_leakage_rate_pct_per_year = data.get("refrigerant_leakage_rate_pct_per_year", None)
        location_of_use = data.get("location_of_use", None)
        # Use serializer to validate and persist minimal model (product_type + weight_kg)
        serializer = EmbodiedCarbonSerializer(data={"product_type": product_type, "weight_kg": weight_kg, "electricity_usage_kwh": electricity_usage_kwh, "location_of_factory": location_of_factory, "lifetime_years": lifetime_years, "refrigerant_used": refrigerant_used, "refrigerant_charge_kg": refrigerant_charge_kg, "refrigerant_leakage_rate_pct_per_year": refrigerant_leakage_rate_pct_per_year, "location_of_use": location_of_use})
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
        a1_val = calculation_total.get("a1_details")
        a2_val = calculation_total.get("a2_details")
        a3_val = calculation_total.get("a3_details")
        a4_val = calculation_total.get("a4_details")
        a1_to_a4_total = a1_val + a2_val + a3_val + a4_val
        c2_val = calculation_total.get("c2_details")
        c3_val = calculation_total.get("c3_details")
        c4_val = calculation_total.get("c4_details")
        c2_to_c4_total = c2_val + c3_val + c4_val   
        b3_stage = (a1_to_a4_total*0.1)+(c2_to_c4_total*0.1)
        buffer_factor=1.3
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
            "b3": b3_stage,
            "with_buffer_factor": (a1_to_a4_total + c2_to_c4_total + b3_stage) * buffer_factor,
            "b1": calculation_total.get("b1_details"),
            "c1": calculation_total.get("c1_details"),
            "b1andc1": calculation_total.get("b1_details") + calculation_total.get("c1_details"),
            "total_embodied_carbon": ((a1_to_a4_total + c2_to_c4_total + b3_stage) * buffer_factor)+ calculation_total.get("b1_details") + calculation_total.get("c1_details"),
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


class EmbodiedCarbonExportPDF(APIView):
    """Export embodied carbon records as a simple PDF report.

    Optional query params (simple filtering): `product_type`, `location_of_factory`.
    For each record we call `calculate_total_embodied_carbon` to include computed totals.
    """
    def get(self, request):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')

        qs = EmbodiedCarbon.objects.all()
        product_type = request.GET.get('product_type')
        location = request.GET.get('location_of_factory')
        if product_type:
            qs = qs.filter(product_type=product_type)
        if location:
            qs = qs.filter(location_of_factory=location)

        # Build PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=pagesizes.A4)
        styles = getSampleStyleSheet()
        elements = []

        title = Paragraph('Embodied Carbon Report', styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Table header
        data = [[
            'ID', 'Product Type', 'Weight (kg)', 'Electricity (kWh)',
            'Factory Location', 'Lifetime (yrs)', 'Refrigerant', 'Refrigerant (kg)',
            'Location of Use', 'Total Embodied Carbon (kgCO2e)'
        ]]

        for obj in qs:
            # attempt to compute totals; if calculation fails include blank
            total_val = ''
            try:
                calc = calculate_total_embodied_carbon(obj)
                # attempt to mirror the summary used in list view
                a1 = calc.get('a1_details', 0) + 0
                a2 = calc.get('a2_details', 0) + 0
                a3 = calc.get('a3_details', 0) + 0
                a4 = calc.get('a4_details', 0) + 0
                a1_to_a4_total = a1 + a2 + a3 + a4
                c2 = calc.get('c2_details', 0) + 0
                c3 = calc.get('c3_details', 0) + 0
                c4 = calc.get('c4_details', 0) + 0
                c2_to_c4_total = c2 + c3 + c4
                b3_stage = (a1_to_a4_total*0.1) + (c2_to_c4_total*0.1)
                buffer_factor = 1.3
                b1 = calc.get('b1_details', 0) + 0
                c1 = calc.get('c1_details', 0) + 0
                total_val = ((a1_to_a4_total + c2_to_c4_total + b3_stage) * buffer_factor) + b1 + c1
                total_val = round(total_val, 4)
            except Exception:
                total_val = 'error'

            data.append([
                str(obj.id),
                obj.product_type or '',
                str(getattr(obj, 'weight_kg', '')),
                str(getattr(obj, 'electricity_usage_kwh', '')),
                obj.location_of_factory or '',
                str(getattr(obj, 'lifetime_years', '')),
                obj.refrigerant_used or '',
                str(getattr(obj, 'refrigerant_charge_kg', '')),
                obj.location_of_use or '',
                str(total_val)
            ])

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