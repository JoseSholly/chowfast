from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('email', 'phone_number', 'user_type', 'is_active', 'is_staff', 'date_joined')
    
    # Fields to filter by in the admin
    list_filter = ('user_type', 'is_active', 'is_staff', 'date_joined')
    
    # Fields to search in the admin
    search_fields = ('email', 'phone_number')
    
    # Fields to order by in the admin
    ordering = ('-date_joined',)
    
    # Fields to display in the admin detail view
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to display when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'user_type', 'password1', 'password2'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')
    
    # Disable username field since it's not used
    filter_horizontal = ('groups', 'user_permissions',)
    
    # Ensure the admin respects the custom USERNAME_FIELD
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'username' in form.base_fields:
            del form.base_fields['username']
        return form