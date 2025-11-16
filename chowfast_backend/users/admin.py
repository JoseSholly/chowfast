from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import OTP, SessionToken, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("email", "phone_number", "user_type", "is_active", "is_activated", "is_staff", "date_joined")
    list_filter = ("user_type", "is_active", "is_activated", "is_staff", "date_joined")
    search_fields = ("email", "phone_number")
    ordering = ("-date_joined",)
    readonly_fields = ("id", "date_joined", "last_login", "last_active")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("phone_number", "user_type")}),
        ("Permissions", {"fields": ("is_active", "is_activated", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_active","last_login", "date_joined")}),
        ("System", {"fields": ("id",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "phone_number", "user_type", "password1", "password2", "is_active", "is_activated", "is_staff"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Regular staff users can only see vendors (non-admin users), unless they are superusers
        if request.user.is_superuser:
            return qs
        return qs.exclude(user_type="admin")

    # Optional: Restrict staff from editing admins
    def has_change_permission(self, request, obj=None):
        if obj and obj.user_type == "admin" and not request.user.is_superuser:
            return False
        return super().has_change_permission(request, obj)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "purpose", "created_at", "is_expired_display")
    list_filter = ("purpose", "created_at")
    search_fields = ("user__email", "user__phone_number")
    readonly_fields = ("user", "code", "purpose", "created_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        # OTPs should only be created programmatically, not via admin
        return False

    def has_change_permission(self, request, obj=None):
        return False  # Prevent editing OTPs

    def has_delete_permission(self, request, obj=None):
        # Allow deletion for cleanup, but be cautious
        return request.user.is_superuser

    def is_expired_display(self, obj):
        return obj.is_expired()
    is_expired_display.boolean = True
    is_expired_display.short_description = "Expired"


@admin.register(SessionToken)
class SessionTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token_short", "purpose", "expires_at", "is_used", "created_at", "is_valid_display")
    list_filter = ("purpose", "is_used", "created_at", "expires_at")
    search_fields = ("user__email", "user__phone_number", "token")
    readonly_fields = ("user", "token", "purpose", "expires_at", "is_used", "created_at", "updated_at")
    ordering = ("-created_at",)

    def has_add_permission(self, request):
        # Session tokens should be created via code, not admin
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def token_short(self, obj):
        return f"{str(obj.token)[:8]}..."
    token_short.short_description = "Token"

    def is_valid_display(self, obj):
        return obj.is_valid()
    is_valid_display.boolean = True
    is_valid_display.short_description = "Valid"