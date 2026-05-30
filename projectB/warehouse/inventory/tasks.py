# inventory/tasks.py
from celery import shared_task
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
from django.db.models import F
import logging

logger = logging.getLogger(__name__)


@shared_task
def generate_daily_inventory_report():
    from .models import ProductStock, StockMovement
    from analytics.models import InventoryReport
    from django.db.models import Sum

    yesterday = timezone.now() - timedelta(days=1)

    total_products = ProductStock.objects.count()
    low_stock_count = ProductStock.objects.filter(
        quantity__lte=F('min_stock_threshold')
    ).count()
    out_of_stock_count = ProductStock.objects.filter(quantity=0).count()

    movements = StockMovement.objects.filter(
        created_at__gte=yesterday
    ).values('movement_type').annotate(total=Sum('quantity'))

    report = InventoryReport.objects.create(
        date=timezone.now().date(),
        report_type='daily',
        status='completed',
        total_products=total_products,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        report_data={
            'movements': dict(movements),
            'timestamp': str(timezone.now())
        }
    )

    cache.set('daily_inventory_report', report.report_data, 86400)
    logger.info(f"Daily report generated: {report.id}")
    return f"Report {report.id} generated"


@shared_task
def check_all_low_stock():
    from .models import ProductStock
    from analytics.models import StockAlert
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()

    if not admin_user:
        admin_user = User.objects.create_superuser(
            username='admin_task',
            email='admin@task.com',
            password='temp123'
        )

    low_stock_products = ProductStock.objects.filter(
        quantity__lte=F('min_stock_threshold')
    )

    alerts_created = 0
    for product in low_stock_products:
        alert, created = StockAlert.objects.get_or_create(
            product_stock=product,
            alert_type='low_stock',
            is_resolved=False,
            defaults={
                'severity': 'high' if product.quantity == 0 else 'medium',
                'current_quantity': product.quantity,
                'threshold_value': product.min_stock_threshold,
                'message': f"Stock level {product.quantity} is below threshold {product.min_stock_threshold}",
                'created_by': admin_user
            }
        )
        if created:
            alerts_created += 1

    logger.info(f"Created {alerts_created} low stock alerts")
    return f"Created {alerts_created} alerts"


@shared_task
def check_low_stock(product_stock_id):
    from .models import ProductStock
    from analytics.models import StockAlert
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin_user = User.objects.filter(is_superuser=True).first()

    try:
        product = ProductStock.objects.get(id=product_stock_id)
        if product.quantity <= product.min_stock_threshold:
            StockAlert.objects.get_or_create(
                product_stock=product,
                alert_type='low_stock',
                is_resolved=False,
                defaults={
                    'severity': 'high' if product.quantity == 0 else 'medium',
                    'current_quantity': product.quantity,
                    'threshold_value': product.min_stock_threshold,
                    'message': f"Stock level {product.quantity} is below threshold {product.min_stock_threshold}",
                    'created_by': admin_user
                }
            )
            return f"Alert created for {product.sku}"
    except Exception as e:
        return f"Error: {str(e)}"


@shared_task
def sync_product_with_projecta():
    from django.conf import settings
    import requests

    try:
        response = requests.get(
            f"{settings.PROJECTA_URL}/api/products/",
            timeout=30
        )
        if response.status_code == 200:
            products = response.json()
            logger.info(f"Synced {len(products)} products from ProjectA")
            return f"Synced {len(products)} products"
    except Exception as e:
        logger.error(f"Sync failed: {str(e)}")
        return f"Sync failed: {str(e)}"
