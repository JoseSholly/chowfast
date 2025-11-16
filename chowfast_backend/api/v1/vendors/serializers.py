import logging

from django.contrib.auth import get_user_model

# from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import OTP, SessionToken
from vendors.email_service import send_signup_otp_email, send_vendor_welcome_email
from vendors.models import Vendor

from .validators import phone_regex, validate_email_address

User = get_user_model()

logger = logging.getLogger(__name__)
class VendorEmailSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    password = serializers.CharField(write_only=True, min_length=8, max_length=75, required=True)

    def validate(self, attrs):
        email = attrs["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is already registered.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            user_type="vendor",
            is_active=True,
            is_activated=False,  # Wait for OTP
        )
        user.set_password(validated_data["password"])
        user.save()

        # Generate OTP
        otp, raw_code = OTP.objects.create_otp(user, purpose="email_verification")

        # Create secure session token (single-use, time-limited)
        session_token = SessionToken.objects.create_token(
            user=user,
            purpose="email_verification",
        )

        # TODO: Send OTP via email
        # Send OTP to user email
        try:
            send_signup_otp_email(user, raw_code)
        except Exception as e:
            logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")

        # print(f"OTP for {user.email}: {raw_code}")  # For testing purposes only

        return {
            "user": user,
            "session_token": str(session_token.token),
        }


class CompleteVendorProfileSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=20, validators=[phone_regex])
    business_name = serializers.CharField(max_length=200)
    address = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("This phone number is already in use.")
        return value

    @transaction.atomic
    def save(self):
        request = self.context["request"]
        user = request.user

        # Update user phone
        user.phone_number = self.validated_data["phone_number"]
        user.save()

        # Create Vendor profile
        vendor = Vendor.objects.create(
            user=user,
            business_name=self.validated_data["business_name"],
            address=self.validated_data.get("address", ""),
        )

        # Mark vendor as verified
        vendor.verified = True
        vendor.save()

        # Send Onboarding mail
        try:
            send_vendor_welcome_email(vendor)
        except Exception as e:
            logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")

        return vendor


class VerifyOTPSerializer(serializers.Serializer):
    session_token = serializers.UUIDField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)

    def validate(self, attrs):
        token_str = str(attrs["session_token"])
        otp_code = attrs["otp"]

        try:
            session_token = SessionToken.objects.get(
                token=token_str,
                purpose="email_verification",
                is_used=False
            )
        except SessionToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired session token.")

        if session_token.is_expired():
            raise serializers.ValidationError("Session token has expired.")

        # Get latest OTP for email verification
        try:
            otp_obj = OTP.objects.filter(
                user=session_token.user,
                purpose="email_verification"
            ).latest("created_at")
        except OTP.DoesNotExist:
            raise serializers.ValidationError("No OTP found.")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        if not otp_obj.verify_otp(otp_code):
            raise serializers.ValidationError("Invalid OTP.")

        attrs["session_token_obj"] = session_token
        attrs["otp_obj"] = otp_obj
        attrs["user"] = session_token.user
        return attrs

    @transaction.atomic
    def verify(self):
        user = self.validated_data["user"]
        session_token = self.validated_data["session_token_obj"]
        otp_obj = self.validated_data["otp_obj"]

        # Mark OTP & session as used
        otp_obj.delete()  # or mark as used
        session_token.is_used = True
        session_token.save()

        # Activate user
        user.is_activated = True
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "user_type": user.user_type,
                "is_activated": user.is_activated,
            }
        }


class ResendOTPSerializer(serializers.Serializer):
    session_token = serializers.UUIDField(required=True)

    def validate(self, attrs):
        token_str = str(attrs["session_token"])
        try:
            session_token = SessionToken.objects.get(
                token=token_str,
                purpose="email_verification",
                is_used=False
            )
        except SessionToken.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired session token.")

        if session_token.is_expired():
            raise serializers.ValidationError("Session has expired. Please sign up again.")

        attrs["user"] = session_token.user
        attrs["session_token_obj"] = session_token
        return attrs

    @transaction.atomic
    def resend(self):
        user = self.validated_data["user"]
        session_token = self.validated_data["session_token_obj"]

        # Delte session and create a new one
        session_token.delete()

        session_token = SessionToken.objects.create_token(
            user=user,
            purpose="email_verification",
        )

        # Generate new OTP
        otp, raw_code = OTP.objects.create_otp(user, purpose="email_verification")

        # Send OTP
        # Send OTP to user email
        try:
            send_signup_otp_email(user, raw_code)
        except Exception as e:
            logger.error(f"Failed to send OTP email to {user.email}: {str(e)}")

        print(f"OTP for {user.email}: {raw_code}")  # For testing purposes only

        return {
            "session_token": str(session_token.token)
        }
    

class CustomLoginSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        errors = {}
        if not email:
            errors["email"] = ["This field is required."]
        if not password:
            errors["password"] = ["This field is required."]
        if errors:
            raise serializers.ValidationError(errors)

        email = email.lower()
        validate_email_address(email)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"non_field_errors": ["Invalid credentials."]})

        if not user.check_password(password):
            raise serializers.ValidationError({"non_field_errors": ["Invalid credentials."]})

        refresh = self.get_token(user)

        # Efficient one-query update
        User.objects.filter(pk=user.pk).update(last_login=timezone.now())

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": user,
        }