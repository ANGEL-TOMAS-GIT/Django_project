from rest_framework.viewsets import ModelViewSet
from .tasks import check_all_low_stock
from rest_framework import  status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.core.cache import cache
from django.utils.translation import gettext as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db import models
from .models import Warehouse, ProductStock, StockMovement
from .serializers import WarehouseSerializer, ProductStockSerializer, StockMovementSerializer
from .tasks import sync_product_with_projecta
from accounts.permissions import HasGroupPermission


# Base View with common functionality
class BaseWarehouseViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    cache_timeout = 300  # 5 minutes
    
    def get_cached_response(self, cache_key, queryset, serializer_class):
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        
        serializer = serializer_class(queryset, many=True)
        cache.set(cache_key, serializer.data, self.cache_timeout)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete_pattern(f"{self.queryset.model.__name__.lower()}_list")
        return instance


class WarehouseViewSet(BaseWarehouseViewSet):
    queryset = Warehouse.objects.filter(is_active=True)
    serializer_class = WarehouseSerializer
    required_group = ['warehouse_manager', 'admin']
    
    @action(detail=True, methods=['get'])
    def stocks(self, request, pk=None):
        warehouse = self.get_object()
        stocks = warehouse.stocks.all()
        serializer = ProductStockSerializer(stocks, many=True)
        return Response(serializer.data)


class ProductStockViewSet(BaseWarehouseViewSet):
    queryset = ProductStock.objects.select_related('warehouse')
    serializer_class = ProductStockSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['warehouse', 'product_id']
    search_fields = ['sku', 'name']
    ordering_fields = ['quantity', 'last_updated']
    required_group = ['warehouse_manager', 'admin', 'warehouse_staff', 'viewer']
    
    @action(detail=False, methods=['post'])
    def sync_with_projecta(self, request):
        """Synchronize stock with ProjectA products"""
        task = sync_product_with_projecta.delay()
        return Response({
            'message': _('Sync started'),
            'task_id': task.id
        }, status=status.HTTP_202_ACCEPTED)
    
    @action(detail=True, methods=['post'])
    def adjust_stock(self, request, pk=None):
        stock = self.get_object()
        quantity = request.data.get('quantity')
        movement_type = request.data.get('movement_type')
        
        if not quantity or not movement_type:
            return Response(
                {'error': _('quantity and movement_type required')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_quantity = stock.quantity
        
        if movement_type == 'IN':
            stock.quantity += int(quantity)
        elif movement_type == 'OUT':
            if stock.quantity - int(quantity) < 0:
                return Response(
                    {'error': _('Insufficient stock')},
                    status=status.HTTP_400_BAD_REQUEST
                )
            stock.quantity -= int(quantity)
        else:
            return Response(
                {'error': _('Invalid movement_type. Use IN or OUT')},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        stock.save()
        
        # Create movement record
        StockMovement.objects.create(
            product_stock=stock,
            movement_type=movement_type,
            quantity=quantity,
            notes=request.data.get('notes', ''),
            created_by=request.user
        )
        
        # Check low stock
        if stock.quantity <= stock.min_stock_threshold:
            check_all_low_stock .delay(stock.id)
        
        # Clear cache
        cache.delete(f"product_stock_{stock.id}")
        
        return Response(ProductStockSerializer(stock).data)
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        low_stock_items = self.get_queryset().filter(
            quantity__lte=models.F('min_stock_threshold')
        )
        serializer = self.get_serializer(low_stock_items, many=True)
        return Response(serializer.data)


class StockMovementViewSet(BaseWarehouseViewSet):
    queryset = StockMovement.objects.select_related('product_stock', 'created_by')
    serializer_class = StockMovementSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['product_stock', 'movement_type']
    ordering_fields = ['created_at']
    required_group = ['warehouse_manager', 'admin']