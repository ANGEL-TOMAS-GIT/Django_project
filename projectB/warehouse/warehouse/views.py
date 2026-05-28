# warehouse/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from inventory.models import ProductStock, Warehouse, StockMovement
from analytics.models import InventoryReport, StockAlert
from django.db.models import Sum, Count, F

@login_required(login_url='/admin/login/')
def dashboard(request):
    """Main dashboard view"""
    context = {
        'title': _('Dashboard'),
        'total_products': ProductStock.objects.count(),
        'total_warehouses': Warehouse.objects.filter(is_active=True).count(),
        'low_stock_count': ProductStock.objects.filter(
            quantity__lte=F('min_stock_threshold')
        ).count(),
        'active_alerts': StockAlert.objects.filter(is_resolved=False).count(),
        'recent_movements': StockMovement.objects.select_related(
            'product_stock'
        ).order_by('-created_at')[:10],
        'recent_reports': InventoryReport.objects.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)

@login_required
def product_list(request):
    """List all products"""
    products = ProductStock.objects.select_related('warehouse').all()
    context = {
        'title': _('Products'),
        'products': products,
    }
    return render(request, 'inventory/product_list.html', context)

@login_required
def warehouse_list(request):
    """List all warehouses"""
    warehouses = Warehouse.objects.all()
    context = {
        'title': _('Warehouses'),
        'warehouses': warehouses,
    }
    return render(request, 'inventory/warehouse_list.html', context)

@login_required
def report_list(request):
    """List all reports"""
    reports = InventoryReport.objects.select_related('generated_by').all()
    context = {
        'title': _('Reports'),
        'reports': reports,
    }
    return render(request, 'analytics/report_list.html', context)

@login_required
def alert_list(request):
    """List all alerts"""
    alerts = StockAlert.objects.select_related('product_stock', 'created_by').all()
    context = {
        'title': _('Alerts'),
        'alerts': alerts,
    }
    return render(request, 'analytics/alert_list.html', context)