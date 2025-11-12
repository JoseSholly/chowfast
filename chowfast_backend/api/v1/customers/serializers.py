from customers.models import Customer
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
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