from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'id',
            'first_name',
            'last_name',
            'email',
            'password',
            'organization_name',
        ]

    def create(self, validated_data):
        # prefer using email as username when username not provided
        username = validated_data.get('username')
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        email = validated_data.get('email')
        password = validated_data.get('password')
        organization_name = validated_data.get('organization_name', '')

        user = CustomUser.objects.create_user(
            username=username if username else email,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            organization_name=organization_name,
        )
        return user

