# analytics/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.utils import timezone
from datetime import timedelta
from django.db import models
from .models import InventoryReport, StockAlert
from .serializers import InventoryReportSerializer, StockAlertSerializer
from inventory.models import ProductStock


class InventoryReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryReport.objects.all()
    serializer_class = InventoryReportSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['report_type', 'status', 'date']

    @action(detail=False, methods=['get'])
    def latest(self, request):
        report = self.get_queryset().order_by('-date', '-created_at').first()
        serializer = self.get_serializer(report)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
    
        data = {
            'total_reports': InventoryReport.objects.count(),
            'reports_this_week': InventoryReport.objects.filter(date__gte=week_ago).count(),
            'active_alerts': StockAlert.objects.filter(is_resolved=False).count(),
            'low_stock_items': ProductStock.objects.filter(
                quantity__lte=models.F('min_stock_threshold')
            ).count(),
            'total_products': ProductStock.objects.count(),
        }
        return Response(data)


class StockAlertViewSet(viewsets.ModelViewSet):
    queryset = StockAlert.objects.all()
    serializer_class = StockAlertSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['alert_type', 'severity', 'is_resolved']
    search_fields = ['product_stock__sku', 'product_stock__name', 'message']

    @action(detail=False, methods=['get'])
    def active(self, request):
        active_alerts = self.get_queryset().filter(is_resolved=False)
        serializer = self.get_serializer(active_alerts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def resolve(self, request, pk=None):
        alert = self.get_object()
        alert.is_resolved = True
        alert.resolved_at = timezone.now()
        alert.resolved_by = request.user
        alert.resolution_notes = request.data.get('notes', '')
        alert.save()
        return Response({'status': 'resolved'})
