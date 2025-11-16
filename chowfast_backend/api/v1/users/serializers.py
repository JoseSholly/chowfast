from api.v1.vendors.validators import validate_email_address
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


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
    
class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()