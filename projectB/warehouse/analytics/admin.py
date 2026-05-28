# analytics/admin.py
from django.contrib import admin
from .models import InventoryReport, StockAlert


class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'report_type', 'status', 'total_products', 'low_stock_count', 'created_at')
    list_filter = ('report_type', 'status', 'date')
    search_fields = ('notes',)
    readonly_fields = ('created_at', 'updated_at')


class StockAlertAdmin(admin.ModelAdmin):
    list_display = ('product_stock', 'alert_type', 'severity', 'current_quantity', 'is_resolved', 'created_at')
    list_filter = ('alert_type', 'severity', 'is_resolved')
    search_fields = ('product_stock__sku', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_resolved',)


# Register the models
admin.site.register(InventoryReport, InventoryReportAdmin)
admin.site.register(StockAlert, StockAlertAdmin)
