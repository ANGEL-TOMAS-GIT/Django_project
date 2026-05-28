# inventory/admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Warehouse, ProductStock, StockMovement


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_active', 'product_count')
    list_filter = ('is_active',)
    search_fields = ('name', 'location')
    list_editable = ('is_active',)

    def product_count(self, obj):
        count = obj.stocks.count()
        url = reverse('admin:inventory_productstock_changelist') + f'?warehouse__id__exact={obj.id}'
        return format_html('<a href="{}">{} products</a>', url, count)
    product_count.short_description = 'Products'


@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'warehouse', 'quantity', 'stock_status')
    list_filter = ('warehouse',)
    search_fields = ('sku', 'name')
    readonly_fields = ('last_updated',)

    def stock_status(self, obj):
        if obj.quantity <= obj.min_stock_threshold:
            return '⚠️ Low Stock'
        return '✓ Normal'
    stock_status.short_description = 'Status'


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product_stock', 'movement_type', 'quantity', 'created_at')
    list_filter = ('movement_type', 'created_at')
    readonly_fields = ('created_at',)

    def has_change_permission(self, request, obj=None):
        return False