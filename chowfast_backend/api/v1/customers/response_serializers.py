from rest_framework import serializers

from .serializers import CustomerSerializer, CustomerInfoSerializer


class BaseResponseSerializer(serializers.Serializer):
    """
    A generic base serializer for standard API success responses.
    This class should be inherited and customized with a 'data' field.
    """
    status = serializers.CharField(
        read_only=True,
        default="success",
        max_length=10,
        help_text="The status of the response, always 'success' for this serializer."
    )
    message = serializers.CharField(
        read_only=True,
        default="Operation successful.",
        max_length=255,
        help_text="A human-readable message about the result."
    )
    # The 'data' field is intentionally left undefined here.
    # Subclasses must define the 'data' field using the appropriate model/data serializer.




class BaseErrorSerializer(serializers.Serializer):
    """
    A generic base serializer for standard custom API error responses (e.g., HTTP 400, 404, 409).
    Subclasses should override the 'error' field's default message.
    """
    error = serializers.CharField(
        read_only=True,
        default="An unknown error occurred.",
        max_length=255,
        help_text="A human-readable error description."
    )
    
    # You could optionally add a fixed error code field here if your API uses one:
    # code = serializers.IntegerField(read_only=True, default=400)

class CustomerCreationSuccessSerializer(BaseResponseSerializer):
    """
    Specific success response for Customer Creation, inheriting the standard wrapper.
    """
    
    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Customer created successfully.",
        max_length=255,
        help_text="Confirmation message for customer creation."
    )
    
    # Define the 'data' field using the CustomerSerializer
    data = CustomerSerializer(read_only=True)

    # Note: If you don't override 'message', it will use the parent's default.
    # Since you want a specific message, it's overridden here.


class ResponseCustomerInfoSerializer(BaseResponseSerializer):
    """
    Success response for Customer get, inheriting the standard wrapper.
    """
    
    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Customer retrieved successfully.",
        max_length=255,
        help_text="Customer retrieved successfully."
    )
    
    # Define the 'data' field using the CustomerSerializer
    data = CustomerInfoSerializer(read_only=True)

    # Note: If you don't override 'message', it will use the parent's default.
    # Since you want a specific message, it's overridden here.

class DuplicatePhoneErrorSerializer(BaseErrorSerializer):
    """
    Specific error response for a duplicate phone number on customer creation.
    """
    
    # Override the 'error' field to provide the specific default message
    error = serializers.CharField(
        read_only=True,
        default="A customer with this phone number already exists.",
        max_length=255
    )