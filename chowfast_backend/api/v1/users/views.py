from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.permissions import IsActivated

from .response_serializers import (
    UserLoginResponseSerializer,
    UserLogoutResponseSerializer,
)
from .serializers import CustomLoginSerializer, LogOutSerializer


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    @swagger_auto_schema(
        request_body=CustomLoginSerializer,
        tags=["User", "Vendors"],
        operation_description="Vendor login",
        responses={
            status.HTTP_200_OK: UserLoginResponseSerializer,
        },
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get("user")

            if user.is_activated is False:
                return Response(
                    {
                        "status": "error",
                        "message": "User account is not activated. Please contact support",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
            data = serializer.validated_data
            return Response(
                {
                    "status": "success",
                    "message": "Login successful",
                    "token": {
                        "refresh": data.get("refresh"),
                        "access": data.get("access"),
                    },
                    "data": {"user_type": data.get("user").user_type},
                },
                status=status.HTTP_200_OK,
            )

        except serializers.ValidationError as e:
            # Check if non_field_errors exist (invalid credentials)
            non_field_errors = e.detail.get("non_field_errors")
            if non_field_errors:
                return Response(
                    {
                        "status": "error",
                        "message": non_field_errors[0],
                    },
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            # Otherwise, field errors
            return Response(
                {
                    "status": "error",
                    "message": "Validation error",
                    "errors": e.detail,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            return Response(
                {
                    "status": "error",
                    "message": f"An unexpected error occurred: {str(e)}",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated, IsActivated]
    serializer_class = LogOutSerializer

    @swagger_auto_schema(
        request_body=LogOutSerializer,
        tags=["User", "Vendors"],
        operation_description="Vendor login",
        responses={
            status.HTTP_200_OK: UserLogoutResponseSerializer,
        },
    )
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()  # Invalidate the refresh token
            return Response(
                {"status": "success", "message": "Logout successful", "data": None},
                status=status.HTTP_200_OK,
            )
        except Exception:
            return Response(
                {"status": "error", "message": "Logout failed", "data": None},
                status=status.HTTP_400_BAD_REQUEST,
            )
