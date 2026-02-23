from rest_framework import serializers
from .models import EmbodiedCarbon, Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at", "updated_at"]


class EmbodiedCarbonSerializer(serializers.ModelSerializer):
    # accept/return project by name (slug) to keep API friendly for the frontend
    project = serializers.SlugRelatedField(slug_field="name", queryset=Project.objects.all())

    class Meta:
        model = EmbodiedCarbon
        fields = [
            "id",
            "project",
            "product_type",
            "weight_kg",
            "location_of_factory",
            "lifetime_years",
            "location_of_use",
            "electricity_usage_kwh",
            "capacity_kw",
            "refrigerant_used",
            "refrigerant_charge_kg",
        ]
