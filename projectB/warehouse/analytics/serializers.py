# analytics/serializers.py
from rest_framework import serializers
from .models import InventoryReport, StockAlert


class InventoryReportSerializer(serializers.ModelSerializer):
    generated_by_name = serializers.CharField(source='generated_by.username', read_only=True)

    class Meta:
        model = InventoryReport
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class StockAlertSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product_stock.sku', read_only=True)
    product_name = serializers.CharField(source='product_stock.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = StockAlert
        fields = '__all__'
        read_only_fields = ('created_at',)
