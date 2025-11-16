from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .response_serializers import (
    VendorEmailSignUpCompleteResponseSerializer,
    VendorEmailSignUpResponseSerializer,
    VendorSignUpVerifyResponseSerializer,
)
from .serializers import (
    CompleteVendorProfileSerializer,
    CustomLoginSerializer,
    ResendOTPSerializer,
    VendorEmailSignupSerializer,
    VerifyOTPSerializer,
)


class VendorEmailSignupView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VendorEmailSignupSerializer

    @swagger_auto_schema(
        tags=["Vendors"],
        operation_summary="Vendor Email Signup",
        request_body=VendorEmailSignupSerializer,
        responses={
            status.HTTP_201_CREATED: VendorEmailSignUpResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.create(serializer.validated_data)
            return Response(
                {
                    "status": "success",
                    "message": "OTP sent to your email. Please verify to continue.",
                    "session_token": result["session_token"],
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompleteVendorProfileView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ['post']
    serializer_class = CompleteVendorProfileSerializer

    @swagger_auto_schema(
        tags=["Vendors"],
        operation_summary="Complete Vendor Profile after Email Verification",
        request_body=CompleteVendorProfileSerializer,
        responses={
            status.HTTP_200_OK: VendorEmailSignUpCompleteResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"request": request})
        if serializer.is_valid():
            result = serializer.save()
            return Response(
                {
                    "status": "success",
                    "message": "Vendor profile completed successfully.",
                    "data": {
                        "vendor_id": result.vendor_id
                    }
                }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    @swagger_auto_schema(
        tags=["Vendors"],
        operation_summary="Verify OTP for Vendor Account Activation",
        request_body=VerifyOTPSerializer,
        responses={
            status.HTTP_200_OK: VendorSignUpVerifyResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            tokens = serializer.verify()
            return Response(
                {
                    "status": "success",
                    "message": "Vendor Account activated successfully!",
                    "data": tokens,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendOTPView(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResendOTPSerializer
    http_method_names = ["post"]

    @swagger_auto_schema(
        tags=["Vendors"],
        operation_summary="Resend OTP for Vendor Email Verification",
        request_body=ResendOTPSerializer,
        responses={
            status.HTTP_200_OK: VendorEmailSignUpResponseSerializer,
        },
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            result = serializer.resend()
            return Response(
                {
                    "status": "success",
                    "message": "New OTP sent successfully.",
                    "session_token": result["session_token"],
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomLoginSerializer

    @swagger_auto_schema(request_body=CustomLoginSerializer, tags=["User"])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get("user")

            if (user.is_activated is False and user.deactivation_date is not None) or (
                user.is_activated is False and user.deactivation_date is None
            ):
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