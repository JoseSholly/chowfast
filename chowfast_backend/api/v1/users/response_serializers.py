from api.v1.vendors.response_serializers import (
    BaseResponseSerializer,
    BaseUserDetailSerializer,
)
from rest_framework import serializers


class TokenResponseSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="JWT refresh token.",
        default="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    )
    access = serializers.CharField(
        help_text="JWT access token.", default="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )

class UserLoginResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor Creation, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Login successful",
        max_length=255,
        help_text="User login successful",
    )
    token = TokenResponseSerializer(
        read_only=True,
        help_text="Acess and Refresh tokens after login",
    )
    data = BaseUserDetailSerializer(help_text="User type")   


class UserLogoutResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor Creation, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Logout successful",
        max_length=255,
        help_text="User logout successful",
    )