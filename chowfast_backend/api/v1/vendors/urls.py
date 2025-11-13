from django.urls import path

from .views import (
    CompleteVendorProfileView,
    ResendOTPView,
    VendorEmailSignupView,
    VerifyOTPView,
)

urlpatterns = [
    path('signup/', VendorEmailSignupView.as_view(), name='vendor-email-signup'),
    path('signup/complete/', CompleteVendorProfileView.as_view(), name='vendor-complete-profile'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('resend-otp/', ResendOTPView.as_view(), name='resend-otp'),
]