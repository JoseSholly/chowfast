from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    readonly_fields = ('id', 'subtotal')
    fields = ('item', 'name', 'quantity', 'price', 'subtotal')
    can_delete = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'vendor', 'total', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'payment_status', 'vendor')
    search_fields = ('id', 'customer__user__username', 'vendor__business_name', 'delivery_address')
    list_editable = ('status', 'payment_status')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'subtotal', 'total')
    fieldsets = (
        (None, {
            'fields': ('customer', 'vendor', 'status', 'payment_status')
        }),
        ('Financials', {
            'fields': ('subtotal', 'delivery_fee', 'total')
        }),
        ('Details', {
            'fields': ('delivery_address', 'notes')
        }),
        ('Metadata', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [OrderItemInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('vendor')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'item', 'quantity', 'price', 'subtotal')
    list_filter = ('order__vendor',)
    search_fields = ('name', 'item__name', 'order__id')
    readonly_fields = ('id', 'subtotal')
    ordering = ('order',)
    fieldsets = (
        (None, {
            'fields': ('order', 'item', 'name', 'quantity', 'price', 'subtotal')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order__vendor', 'item')