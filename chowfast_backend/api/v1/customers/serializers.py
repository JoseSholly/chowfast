from customers.models import Customer
from django.core.validators import RegexValidator
from rest_framework import serializers

phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message="Phone number must be in international format (e.g. +2348012345678)",
)


class CustomerSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        required=True, max_length=20, validators=[phone_regex]
    )

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "phone_number",
            "location",
            "delivery_address",
            "created_at",
        ]
        read_only_fields = ["customer_id", "created_at"]
        extra_kwargs = {
            "phone_number": {
                "required": True,
                "error_messages": {
                    "unique": "This phone number is already registered."
                },
            },
            "location": {"required": True},
            "delivery_address": {"required": True},
        }


class CustomerInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "phone_number",
            "location",
            "delivery_address",
        ]
        read_only_fields = fields
