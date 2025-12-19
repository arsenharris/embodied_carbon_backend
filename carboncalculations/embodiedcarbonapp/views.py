from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import EmbodiedCarbonSerializer, ProjectSerializer
from .models import Project
from django.http import HttpResponse
from django.apps import apps
from rest_framework import status
from .data.material_reference import MATERIAL_COEFFS, PRESET_PERCENTAGES
from .data.reference_data import  PRODUCT_LIST,MANUFACTURING_LOCATION,REFRIGERANT_GWP,INSTALLATION_LOCATION
from .calculations.calculations import (calculate_a1_from_instance, calculate_a2_from_instance,calculate_a3_from_instance, calculate_a4_from_instance,calculate_b1andc1_from_instance, calculate_c2_from_instance, calculate_c3_from_instance, calculate_c4_from_instance)
from .data.logic import product_requirements
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
        product_type_raw = data.get("product_type")
        if not product_type_raw:
            return Response({"error": "product_type is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        product_info = self.get_product(product_type_raw)
        product_type = product_info["product"]
        
        required_fields = product_requirements.get(product_type.lower(), [])

        # project: accept either `project` (name) or legacy `project_name`.
        project_name = data.get("project") or data.get("project_name")
        if not project_name and "project_name" in required_fields:
            return Response({"error": "project_name is required for {product_type}"}, status=status.HTTP_400_BAD_REQUEST)

        # ensure Project exists (create if missing)
        if project_name:
            project_obj, _ = Project.objects.get_or_create(name=project_name)

        serializer_data = {}
        for field in required_fields:
            # map incoming 'project_name' to serializer field 'project'
            if field == "project_name":
                # serializer expects project by name (SlugRelatedField)
                serializer_data["project"] = project_obj.name
                continue
            value = data.get(field)
            if value is None:
                return Response({"error": f"{field} is required for {product_type}"}, status=status.HTTP_400_BAD_REQUEST)
            serializer_data[field] = value
        
        serializer = EmbodiedCarbonSerializer(data=serializer_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        instance = serializer.save()
    
        materials_override = data.get("materials_override") or data.get("materials")

        if materials_override and isinstance(materials_override, dict):
            setattr(instance, 'materials_override', materials_override)

        tier = "professional"
        scaleup_factor = 1.6
        buffer_factor = 1.3
        try:
            if tier == 'freetier':
                a1_val_free = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                return Response({ "id": instance.id, "a1": a1_val_free,}, status=status.HTTP_201_CREATED)

            if tier == 'basic':
                    a1_val = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    total_a1_replaced=(a1_val)*0.1
                    a1_together=(a1_val+total_a1_replaced)
                    remaining_life_cycle_stages=a1_together*scaleup_factor
                    conservative_buffer_factor=remaining_life_cycle_stages*buffer_factor
                    b1_c1_result = calculate_b1andc1_from_instance(instance) if instance.refrigerant_used and instance.refrigerant_charge_kg else {'total_b1': 0.0, 'total_c1': 0.0}
                    total_b1 = b1_c1_result.get("total_b1", 0.0)
                    total_c1 = b1_c1_result.get("total_c1", 0.0)
                    b1_c1_val= total_b1 + total_c1
                    annual_leakage_rate_b1_use = b1_c1_result.get('annual_leakage_rate_b1_use', 0.0)
                    end_of_life_leakage_rate_c1_deconstruction = b1_c1_result.get('end_of_life_leakage_rate_c1_deconstruction', 0.0)
                    basic_total=conservative_buffer_factor + b1_c1_val

                    return Response({ 
                        "id": instance.id,
                        "a1": a1_val, 
                        "total a1 replaced": total_a1_replaced,
                        "a1 together ":a1_together,
                        "remaining life cycle stages":remaining_life_cycle_stages, 
                        "conservative buffer factor": conservative_buffer_factor, 
                        "b1": total_b1,
                        "c1": total_c1,
                        "b1_c1": b1_c1_val,
                        "annual_leakage_rate_b1_use":annual_leakage_rate_b1_use,
                        "end_of_life_leakage_rate_c1_deconstruction":end_of_life_leakage_rate_c1_deconstruction,
                        "basic_total": basic_total   
                        }, status=status.HTTP_201_CREATED)
            
            if tier == 'professional':
                    a1_val_pro = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                    a2_val_pro = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                    a3_val_pro = float(calculate_a3_from_instance(instance).get('total_a3', 0.0)) if instance.electricity_usage_kwh is not None else 0.0
                    a4_val_pro = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))
                    total_a1_to_a4_pro=(a1_val_pro+a2_val_pro+a3_val_pro+a4_val_pro)
                    total_c2_pro = calculate_c2_from_instance(instance).get("total_c2", 0.0)
                    total_c3_pro = calculate_c3_from_instance(instance).get("total_c3", 0.0) if instance.electricity_usage_kwh is not None else 0.0
                    total_c4_pro = calculate_c4_from_instance(instance).get("total_c4", 0.0)
                    c2_to_c4_pro = total_c2_pro + total_c3_pro + total_c4_pro
                    b3_val_pro = (total_a1_to_a4_pro * 0.1)+(c2_to_c4_pro*0.1)
                    with_buffer_pro=(total_a1_to_a4_pro+c2_to_c4_pro+b3_val_pro)*buffer_factor
                    b1_c1_result_pro = calculate_b1andc1_from_instance(instance) if instance.refrigerant_used and instance.refrigerant_charge_kg else {'total_b1': 0.0, 'total_c1': 0.0}
                    total_b1_pro = b1_c1_result_pro.get("total_b1", 0.0)
                    total_c1_pro = b1_c1_result_pro.get("total_c1", 0.0)
                    b1_c1_val_pro= total_b1_pro + total_c1_pro
                    mid_level=with_buffer_pro + b1_c1_val_pro

                    return Response({
                        "id": instance.id,
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


class ProductRequirements(APIView):
    ''' getting required fields for a product type '''
    def get(self, request):
        product_type = request.GET.get("product_type")
        if not product_type:
            return Response({"error": "product_type is required"}, status=400)
        
        normalized = product_type.strip().lower()
        required = product_requirements.get(normalized, [])
        return Response({"required_fields": required}, status=status.HTTP_200_OK)


class ProjectsList(APIView):
    """Return a list of all Projects (used as home page data)."""
    def get(self, request):
        projects = Project.objects.all().order_by("name")
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetail(APIView):
    """Return a single Project and its related products (EmbodiedCarbon records)."""
    def get(self, request, id):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')
        project = Project.objects.filter(id=id).first()
        if not project:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

        products = EmbodiedCarbon.objects.filter(project=project)
        project_data = ProjectSerializer(project).data
        products_data = EmbodiedCarbonSerializer(products, many=True).data

        return Response({"project": project_data, "products": products_data}, status=status.HTTP_200_OK)


class CompareProducts(APIView):
    """Compare two existing `EmbodiedCarbon` records side-by-side.

    POST payload options:
    - {"left_id": 1, "right_id": 2}
    - or provide list: {"ids": [1, 2]}

    Response contains per-stage results for each record, normalized metrics
    (per kW, per kg when available), and absolute + percent differences.
    """
    def post(self, request):
        EmbodiedCarbon = apps.get_model('embodiedcarbonapp.EmbodiedCarbon')

        left_id = request.data.get('left_id')
        right_id = request.data.get('right_id')
        ids = request.data.get('ids')
        if ids and isinstance(ids, (list, tuple)) and len(ids) >= 2:
            left_id, right_id = ids[0], ids[1]

        if not left_id or not right_id:
            return Response({"error": "Provide 'left_id' and 'right_id' or 'ids':[left,right]"}, status=status.HTTP_400_BAD_REQUEST)

        left = EmbodiedCarbon.objects.filter(id=left_id).first()
        right = EmbodiedCarbon.objects.filter(id=right_id).first()
        if not left or not right:
            return Response({"error": "One or both records not found"}, status=status.HTTP_404_NOT_FOUND)

        def metrics_for(instance):
            a1 = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
            a2 = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
            a3 = float(calculate_a3_from_instance(instance).get('total_a3', 0.0)) if getattr(instance, 'electricity_usage_kwh', None) is not None else 0.0
            a4 = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))
            c2 = float(calculate_c2_from_instance(instance).get('total_c2', 0.0))
            c3 = float(calculate_c3_from_instance(instance).get('total_c3', 0.0)) if getattr(instance, 'electricity_usage_kwh', None) is not None else 0.0
            c4 = float(calculate_c4_from_instance(instance).get('total_c4', 0.0))
            b1c1 = calculate_b1andc1_from_instance(instance) if getattr(instance, 'refrigerant_used', None) and getattr(instance, 'refrigerant_charge_kg', None) else {'total_b1': 0.0, 'total_c1': 0.0}
            b1 = float(b1c1.get('total_b1', 0.0))
            c1 = float(b1c1.get('total_c1', 0.0))

            total_no_refrigerant = a1 + a2 + a3 + a4 + c2 + c3 + c4
            total_with_refrigerant = total_no_refrigerant + b1 + c1

            # normalizations
            per_kw = None
            if getattr(instance, 'capacity_kw', None):
                per_kw = {
                    'total_no_refrigerant_per_kw': total_no_refrigerant / float(instance.capacity_kw),
                    'total_with_refrigerant_per_kw': total_with_refrigerant / float(instance.capacity_kw)
                }
            per_kg = None
            if getattr(instance, 'weight_kg', None):
                per_kg = {
                    'total_no_refrigerant_per_kg': total_no_refrigerant / float(instance.weight_kg),
                    'total_with_refrigerant_per_kg': total_with_refrigerant / float(instance.weight_kg)
                }

            return {
                'id': instance.id,
                'product_type': instance.product_type,
                'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4,
                'b1': b1, 'c1': c1,
                'c2': c2, 'c3': c3, 'c4': c4,
                'total_no_refrigerant': total_no_refrigerant,
                'total_with_refrigerant': total_with_refrigerant,
                'per_kw': per_kw,
                'per_kg': per_kg,
            }

        left_metrics = metrics_for(left)
        right_metrics = metrics_for(right)

        def diff(a, b):
            try:
                abs_diff = b - a
                pct = (abs_diff / a * 100.0) if a != 0 else None
                return {'absolute': abs_diff, 'percent': pct}
            except Exception:
                return {'absolute': None, 'percent': None}

        comparison = {
            'left': left_metrics,
            'right': right_metrics,
            'differences': {
                'total_no_refrigerant': diff(left_metrics['total_no_refrigerant'], right_metrics['total_no_refrigerant']),
                'total_with_refrigerant': diff(left_metrics['total_with_refrigerant'], right_metrics['total_with_refrigerant']),
            }
        }

        # if normalization available for both sides, include normalized diffs
        if left_metrics.get('per_kw') and right_metrics.get('per_kw'):
            comparison['differences']['total_no_refrigerant_per_kw'] = diff(left_metrics['per_kw']['total_no_refrigerant_per_kw'], right_metrics['per_kw']['total_no_refrigerant_per_kw'])
            comparison['differences']['total_with_refrigerant_per_kw'] = diff(left_metrics['per_kw']['total_with_refrigerant_per_kw'], right_metrics['per_kw']['total_with_refrigerant_per_kw'])

        if left_metrics.get('per_kg') and right_metrics.get('per_kg'):
            comparison['differences']['total_no_refrigerant_per_kg'] = diff(left_metrics['per_kg']['total_no_refrigerant_per_kg'], right_metrics['per_kg']['total_no_refrigerant_per_kg'])
            comparison['differences']['total_with_refrigerant_per_kg'] = diff(left_metrics['per_kg']['total_with_refrigerant_per_kg'], right_metrics['per_kg']['total_with_refrigerant_per_kg'])

        return Response(comparison, status=status.HTTP_200_OK)

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

        # Add a simple header row for product information and value
        data = [
            ["Product Information", "Value"],
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
            # Header row styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            # Body row background
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))

        elements.append(table)
        # If basic tier was requested, add a separate table with basic-tier embodied carbon results
        if tier == 'basic':
            try:
                # Use same scale and buffer factors as in the API calculation path
                scaleup_factor = 1.6
                buffer_factor = 1.3

                a1_val = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                a2_val = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                a3_val = float(calculate_a3_from_instance(instance).get('total_a3', 0.0))
                a4_val = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))

                # Transport / end-of-life stages
                c2_val = float(calculate_c2_from_instance(instance).get('total_c2', 0.0))
                c3_val = float(calculate_c3_from_instance(instance).get('total_c3', 0.0))
                c4_val = float(calculate_c4_from_instance(instance).get('total_c4', 0.0))

                # Derive B3 as 10% of (A1-A4 + C2-C4) (same approach used elsewhere)
                total_a1_to_a4 = a1_val + a2_val + a3_val + a4_val
                total_c2_to_c4 = c2_val + c3_val + c4_val
                b3_val = 0.1 * (total_a1_to_a4 + total_c2_to_c4)

                # A1 components replaced in B3 are assumed to be 10% of A1 (consistent with replacement factor)
                a1_components_replaced = a1_val * 0.1

                # Total of A1–A4, B3, C2–C4 before scaling
                total_no_refrigerant = total_a1_to_a4 + total_c2_to_c4 + b3_val

                # Apply scale-up and buffer factors
                scaled = total_no_refrigerant * scaleup_factor
                buffered = scaled * buffer_factor

                basic_table_data = [
                    ["Embodied carbon results (kgCO2e) — without refrigerant leakage", ""],
                    ["A1: Material extraction (original product)", f"{a1_val:.2f}"],
                    ["A1: Material extraction (components that are\nreplaced in B3)", f"{a1_components_replaced:.2f}"],
                    ["A1–A4, B3, C2–C4: Total embodied carbon\nwith scale-up and buffer factors (excluding\nrefrigerant leakage)", f"{buffered:.2f}"],
                ]

                basic_table = Table(basic_table_data, colWidths=[300, 200])
                basic_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))

                elements.append(Spacer(1, 12))
                elements.append(basic_table)

                # Refrigerant leakage only (B1 + C1)
                b1c1 = calculate_b1andc1_from_instance(instance)
                total_b1 = float(b1c1.get('total_b1', 0.0))
                total_c1 = float(b1c1.get('total_c1', 0.0))
                total_b1_c1 = total_b1 + total_c1

                refrigerant_table_data = [
                    ["Embodied carbon result (kgCO2e) — refrigerant leakage only", ""],
                    ["B1 (refrigerant leakage during use) + C1 (refrigerant leakage end of life)", f"{total_b1_c1:.2f}"],
                ]
                refrigerant_table = Table(refrigerant_table_data, colWidths=[300, 200])
                refrigerant_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))

                elements.append(Spacer(1, 12))
                elements.append(refrigerant_table)

                # Embodied carbon result with basic calculation method (A1–C4 total)
                basic_method_total = total_a1_to_a4 + total_c2_to_c4
                basic_total_table_data = [
                    ["Embodied carbon result with basic calculation method (kgCO2e) — total", ""],
                    ["A1–C4", f"{basic_method_total:.2f}"],
                ]
                basic_total_table = Table(basic_total_table_data, colWidths=[300, 200])
                basic_total_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))

                elements.append(Spacer(1, 12))
                elements.append(basic_total_table)

                # Assumptions table
                assumptions_data = [
                    ["Assumptions", ""],
                    ["A1: Material carbon coefficient source", "CIBSE guide TM65ANZ Table 2.3"],
                    ["B1: Refrigerant annual leakage rate (%)", "9% TM65ANZ assumptions"],
                    ["C1: End of life leakage rate (%)", "30% TM65ANZ assumptions"],
                    ["B3: Proportion of materials replaced as part of repair (%)", "10% TM65ANZ assumptions"],
                ]
                assumptions_table = Table(assumptions_data, colWidths=[300, 200])
                assumptions_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))

                elements.append(Spacer(1, 12))
                elements.append(assumptions_table)
            except Exception:
                # If any calculation fails, continue without the basic-tier table
                pass
        # Mid-level report section: notes, product info, detailed stage breakdown, refrigerant only and mid-level total
        if tier == 'professional':
            try:
                notes_data = [
                    ["Mid-level calculation Notes/source", ""],
                    ["Date of assessment", request.GET.get('date_of_assessment', 'dd.mm.yy')],
                    ["Name of assessor and assessor organisation", request.GET.get('assessor_name', 'Example for guide')],
                    ["Contact details of assessor", request.GET.get('assessor_contact', 'Example for guide')],
                    ["Country", request.GET.get('country', 'Australia')],
                    ["Calculations based on", "TM65ANZ"],
                ]
                notes_table = Table(notes_data, colWidths=[300, 200])
                notes_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(notes_table)

                # Product information (reuse instance fields, fallback to example values)
                product_complexity = getattr(instance, 'product_complexity_category', None) or request.GET.get('product_complexity', 'Category 3')
                material_95 = 'Y' if request.GET.get('material_95', None) in (None, '', 'Y', 'y', 'yes') else request.GET.get('material_95')
                product_info = [
                    ["Product information", "Value"],
                    ["Type of product", instance.product_type or 'Heat Pump'],
                    ["Capacity", f"{instance.capacity_kw} kW" if getattr(instance, 'capacity_kw', None) else request.GET.get('capacity', '100 kW')],
                    ["Product weight (kg)", f"{instance.weight_kg} kg" if getattr(instance, 'weight_kg', None) else request.GET.get('weight_kg', '1000 kg')],
                    ["Material % breakdown for at least 95% of the product weight? (Y/N)", material_95],
                    ["Product service life (years)", f"{instance.lifetime_years}" if getattr(instance, 'lifetime_years', None) else request.GET.get('lifetime_years', '15')],
                    ["If refrigerant based, type of refrigerant used", refrigerant_display],
                    ["Refrigerant charge (kg)", f"{instance.refrigerant_charge_kg} kg" if getattr(instance, 'refrigerant_charge_kg', None) else request.GET.get('refrigerant_charge_kg', '35 kg')],
                    ["Energy consumption of the factory per unit of product", f"{instance.electricity_usage_kwh} kW·h" if getattr(instance, 'electricity_usage_kwh', None) else request.GET.get('electricity_usage_kwh', '200 kW·h')],
                    ["Location of factory – final assembly location", getattr(instance, 'location_of_factory', request.GET.get('location_of_factory', 'China, Asia'))],
                    ["Product complexity category", product_complexity],
                ]
                prod_table = Table(product_info, colWidths=[300, 200])
                prod_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(prod_table)

                # Detailed stage breakdown (A1..C4). Use calculations where available; show 'n/a' where not applicable.
                a1 = float(calculate_a1_from_instance(instance).get('total_a1', 0.0))
                a2 = float(calculate_a2_from_instance(instance).get('total_a2', 0.0))
                a3 = float(calculate_a3_from_instance(instance).get('total_a3', 0.0))
                a4 = float(calculate_a4_from_instance(instance).get('total_a4', 0.0))
                # A5, B2, B4..B7 may not be modelled; mark n/a
                b1 = float(calculate_b1andc1_from_instance(instance).get('total_b1', 0.0))
                b3 = 0.0
                # For mid-level B3 use 10% of (A1–A4 + C2–C4)
                total_a1_to_a4 = a1 + a2 + a3 + a4
                c2 = float(calculate_c2_from_instance(instance).get('total_c2', 0.0))
                c3 = float(calculate_c3_from_instance(instance).get('total_c3', 0.0))
                c4 = float(calculate_c4_from_instance(instance).get('total_c4', 0.0))
                # B3 assume 10% of (A1–A4 + C2–C4)
                b3 = 0.1 * (total_a1_to_a4 + c2 + c3 + c4)
                c1 = float(calculate_b1andc1_from_instance(instance).get('total_c1', 0.0))

                breakdown_data = [
                    ["Embodied carbon results (kgCO2e) — without refrigerant leakage", ""],
                    ["A1: Material extraction", f"{a1:.2f} TM65ANZ assumptions"],
                    ["A2: Transport", f"{a2:.2f} TM65ANZ assumptions"],
                    ["A3: Manufacturing", f"{a3:.2f} TM65ANZ assumptions"],
                    ["A4: Transport to site", f"{a4:.2f} TM65ANZ assumptions"],
                    ["A5: Construction", "n/a"],
                    ["B1: Use", f"{b1:.2f} TM65ANZ type B"],
                    ["B2: Maintenance", "n/a"],
                    ["B3: Repair", f"{b3:.2f} TM65ANZ assumptions"],
                    ["B4: Replacement", "n/a"],
                    ["B5: Refurbishment", "n/a"],
                    ["B6: Operational energy", "n/a"],
                    ["B7: Operational water", "n/a"],
                    ["C1: Deconstruction", f"{c1:.2f} TM65ANZ type B"],
                    ["C2: Transport", f"{c2:.2f} TM65ANZ assumptions"],
                    ["C3: Waste processing", f"{c3:.2f} TM65ANZ assumptions"],
                    ["C4: Disposal", f"{c4:.2f} TM65ANZ"],
                ]
                breakdown_table = Table(breakdown_data, colWidths=[300, 200])
                breakdown_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(breakdown_table)

                # A1–C4 excluding B1,C1 and with buffer
                total_no_refrigerant = total_a1_to_a4 + c2 + c3 + c4
                total_with_buffer = total_no_refrigerant * buffer_factor
                totals_data = [
                    ["Embodied carbon result (kgCO2e) — without refrigerant leakage", ""],
                    ["A1–C4 (Excluding B1,C1)", f"{total_no_refrigerant:.2f}"],
                    ["A1–C4 with buffer factor (excluding B1, C1)", f"{total_with_buffer:.2f}"],
                ]
                totals_table = Table(totals_data, colWidths=[300, 200])
                totals_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(totals_table)

                # Refrigerant leakage only
                total_b1_c1 = b1 + c1
                refrigerant_only = [
                    ["Embodied carbon result (kgCO2e) — refrigerant leakage only", ""],
                    ["B1 (refrigerant leakage during use) + C1 (refrigerant leakage end of life)", f"{total_b1_c1:.2f}"],
                ]
                refrigerant_only_table = Table(refrigerant_only, colWidths=[300, 200])
                refrigerant_only_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(refrigerant_only_table)

                # Mid-level total (follow professional mid-level math)
                c2_to_c4 = c2 + c3 + c4
                b3_mid = (total_a1_to_a4 * 0.1) + (c2_to_c4 * 0.1)
                with_buffer_mid = (total_a1_to_a4 + c2_to_c4 + b3_mid) * buffer_factor
                mid_level_total = with_buffer_mid + total_b1_c1
                mid_level_table_data = [
                    ["Embodied carbon result with mid-level calculation method (kgCO2e) — total", ""],
                    ["Result of mid-level calculation", f"{mid_level_total:.2f}"],
                ]
                mid_level_table = Table(mid_level_table_data, colWidths=[300, 200])
                mid_level_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(mid_level_table)

                # Assumptions table (mid-level)
                assumptions_mid = [
                    ["Assumptions", ""],
                    ["A1: Material carbon coefficient source", "TM65ANZ Table 2.3"],
                    ["B1: Refrigerant annual leakage rate (%)", "9% TM65ANZ type B"],
                    ["C1: End of life leakage rate (%)", "30% TM65ANZ type B"],
                    ["B3: Materials replaced as part of repair (%)", "10% TM65ANZ assumption"],
                    ["C4: Percentage of product going to landfill (%)", "30% TM65ANZ assumption"],
                ]
                assumptions_mid_table = Table(assumptions_mid, colWidths=[300, 200])
                assumptions_mid_table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('LEFTPADDING', (0, 0), (-1, -1), 8),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(Spacer(1, 12))
                elements.append(assumptions_mid_table)
            except Exception:
                pass
        doc.build(elements)

        buffer.seek(0)
        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="embodied_carbon_report.pdf"'
        return response