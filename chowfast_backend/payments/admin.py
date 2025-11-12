from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'transaction_ref', 'status', 'amount', 'paid_at', 'created_at')
    list_filter = ('status',)
    search_fields = ('id', 'transaction_ref', 'order__id')
    list_editable = ('status',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'paid_at')
    fieldsets = (
        (None, {
            'fields': ('order', 'transaction_ref', 'status', 'amount')
        }),
        ('Dates', {
            'fields': ('paid_at', 'created_at')
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')