from api.v1.customers.response_serializers import BaseResponseSerializer
from rest_framework import serializers


class VendorEmailSignUpResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor Creation, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="OTP sent to your email. Please verify to continue.",
        max_length=255,
        help_text="Confirmation message for vendor creation.",
    )

    session_token = serializers.UUIDField(
        read_only=True, help_text="Session token for OTP verification."
    )

class BaseUserDetailSerializer(serializers.Serializer):
    user_type = serializers.CharField(help_text="Type of user (e.g., 'vendor').")
class UserDetailSerializer(BaseUserDetailSerializer):
    user_type = serializers.CharField(help_text="Type of user (e.g., 'vendor').")
    is_activated = serializers.BooleanField(
        help_text="Indicates if the account has been activated."
    )


class ActivationDetailSerializer(serializers.Serializer):
    refresh = serializers.CharField(
        help_text="JWT refresh token.",
        default="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    )
    access = serializers.CharField(
        help_text="JWT access token.", default="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    user = UserDetailSerializer(help_text="Details of the activated user.")


class VendorSignUpVerifyResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor activation, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Vendor Account activated successfully!",
    )
    data = ActivationDetailSerializer(
        read_only=True,
        help_text="Details of the activated vendor account.",
    )

class VendorEmailSignUpCompleteResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor Sign Up, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="Vendor profile completed successfully.",
    )
    data = serializers.DictField(
        read_only=True,
        help_text="Details of the activated vendor account.",
    )

class LogoutResponseSerializer(BaseResponseSerializer):
    """
    Specific success response for Vendor Creation, inheriting the standard wrapper.
    """

    # Override the 'message' field with the specific default
    message = serializers.CharField(
        read_only=True,
        default="OTP sent to your email. Please verify to continue.",
        max_length=255,
        help_text="Confirmation message for vendor creation.",
    )

    session_token = serializers.UUIDField(
        read_only=True, help_text="Session token for OTP verification."
    )