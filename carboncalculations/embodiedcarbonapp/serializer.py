from rest_framework import serializers
from .models import EmbodiedCarbon  # direct import


class EmbodiedCarbonSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmbodiedCarbon
        fields = '__all__'
