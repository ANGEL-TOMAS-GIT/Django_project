from rest_framework import serializers
from .models import Warehouse, ProductStock, StockMovement


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class ProductStockSerializer(serializers.ModelSerializer):
    available_quantity = serializers.IntegerField(read_only=True)
    warehouse_name = serializers.CharField(source='warehouse.name', read_only=True)

    class Meta:
        model = ProductStock
        fields = '__all__'
        read_only_fields = ['last_updated']


class StockMovementSerializer(serializers.ModelSerializer):
    product_sku = serializers.CharField(source='product_stock.sku', read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = StockMovement
        fields = '__all__'
        read_only_fields = ['created_at']
