"""
URL configuration for chowfast_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# 1. Define the Schema View (Restricted Access)
schema_view = get_schema_view(
    openapi.Info(
        title="ChowFast Food Delivery API",
        default_version="v1",
        description="API documentation for the ChowFast platform.",
        terms_of_service="https://www.yourdomain.com/terms/",
        contact=openapi.Contact(email="support@yourdomain.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Get a new access and refresh token pair (Login)
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Get a new access token using the refresh token
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Optional: Verify a token's validity
    path("api/v1/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path(
        "api/swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "api/redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("api/v1/customers/", include("api.v1.customers.urls")),
    path("api/v1/vendors/", include("api.v1.vendors.urls")),
    path("api/v1/users/", include("api.v1.users.urls")),
]
