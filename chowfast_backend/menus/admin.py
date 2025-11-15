from django.contrib import admin

from .models import MenuItem


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'price', 'available', 'created_at', 'image_preview')
    list_filter = ('vendor', 'category', 'available')
    search_fields = ('name', 'description', 'vendor__business_name')
    list_editable = ('price', 'available', 'category')
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('vendor', 'name', 'category', 'price', 'available')
        }),
        ('Details', {
            'fields': ('description', 'image', 'image_preview')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vendor')

    def image_preview(self, obj):
        if obj.image_url:
            return admin.utils.format_html('<img src="{}" style="max-height: 50px;"/>', obj.image_url)
        return "-"
    image_preview.short_description = "Image"