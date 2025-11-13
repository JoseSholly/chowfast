from customers.models import Customer
from rest_framework import serializers
from api.v1.vendors.validators import phone_regex

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
