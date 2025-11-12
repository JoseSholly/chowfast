from django.contrib import admin

from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('customer_id', 'phone_number', 'location', 'created_at')
    
    # Fields to filter by in the admin
    list_filter = ('created_at',)
    
    # Fields to search in the admin
    search_fields = ('customer_id', 'phone_number', 'location')
    
    # Fields to order by in the admin
    ordering = ('-created_at',)
    
    # Fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('customer_id', 'phone_number', 'location', 'delivery_address')}),
        ('Dates', {'fields': ('created_at',)}),
    )
    
    # Read-only fields
    readonly_fields = ('customer_id', 'created_at')