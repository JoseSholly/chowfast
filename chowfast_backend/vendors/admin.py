from django.contrib import admin

from .models import Vendor


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('vendor_id', 'business_name', 'user_email', 'rating', 'total_orders', 'online', 'verified', 'created_at')
    
    # Fields to filter by in the admin
    list_filter = ('online', 'verified', 'created_at')
    
    # Fields to search in the admin
    search_fields = ('vendor_id', 'business_name', 'user__email')
    
    # Fields to order by in the admin
    ordering = ('-created_at',)
    
    # Fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('vendor_id', 'user', 'business_name', 'address')}),
        ('Status', {'fields': ('online', 'verified')}),
        ('Metrics', {'fields': ('rating', 'total_orders')}),
        ('Dates', {'fields': ('created_at',)}),
    )
    
    # Read-only fields
    readonly_fields = ('vendor_id', 'created_at', 'total_orders')
    
    # Custom method to display user's email in list view
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User Email'