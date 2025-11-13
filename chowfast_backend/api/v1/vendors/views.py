from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
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
