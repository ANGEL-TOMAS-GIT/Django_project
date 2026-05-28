# analytics/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from inventory.models import ProductStock, Warehouse
from .models import InventoryReport, StockAlert

User = get_user_model()


class AnalyticsModelTests(TestCase):
    """Tests for Analytics Models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        
        self.warehouse = baker.make(Warehouse)
        self.product = baker.make(ProductStock, warehouse=self.warehouse)
    
    def test_create_inventory_report(self):
        report = InventoryReport.objects.create(
            date='2026-05-27',
            report_type='daily',
            status='completed',
            total_products=10,
            low_stock_count=2,
            generated_by=self.user
        )
        
        self.assertEqual(report.report_type, 'daily')
        self.assertEqual(report.total_products, 10)
        self.assertEqual(str(report), 'Daily Report - 2026-05-27')
    
    def test_create_stock_alert(self):
        alert = StockAlert.objects.create(
            product_stock=self.product,
            alert_type='low_stock',
            severity='high',
            current_quantity=5,
            threshold_value=10,
            message='Low stock alert',
            created_by=self.user
        )
        
        self.assertEqual(alert.alert_type, 'low_stock')
        self.assertEqual(alert.severity, 'high')
        self.assertEqual(str(alert), f'Low Stock - {self.product.sku} - high')
    
    def test_resolve_alert(self):
        alert = StockAlert.objects.create(
            product_stock=self.product,
            alert_type='low_stock',
            severity='medium',
            current_quantity=5,
            threshold_value=10,
            message='Test alert',
            created_by=self.user
        )
        
        self.assertFalse(alert.is_resolved)
        
        alert.is_resolved = True
        alert.save()
        
        self.assertTrue(alert.is_resolved)


class AnalyticsAPITests(APITestCase):
    """Tests for Analytics API"""
    
    def setUp(self):
        # Create user and group
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        from django.contrib.auth.models import Group
        group, _ = Group.objects.get_or_create(name='warehouse_manager')
        self.user.groups.add(group)
        
        # Get JWT token
        response = self.client.post('/api/auth/token/', {
            'username': 'testuser',
            'password': 'testpass123'
        }, format='json')
        
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create test data
        self.warehouse = baker.make(Warehouse)
        self.product = baker.make(ProductStock, warehouse=self.warehouse)
        self.report = baker.make(InventoryReport, generated_by=self.user)
        self.alert = baker.make(StockAlert, product_stock=self.product, created_by=self.user)
    
    def test_list_reports(self):
        url = reverse('inventoryreport-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_latest_report(self):
        url = reverse('inventoryreport-latest')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)
    
    def test_get_report_summary(self):
        url = reverse('inventoryreport-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_reports', response.data)
        self.assertIn('active_alerts', response.data)
    
    def test_list_alerts(self):
        url = reverse('stockalert-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_active_alerts(self):
        url = reverse('stockalert-active')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_resolve_alert(self):
        alert = baker.make(StockAlert, product_stock=self.product, is_resolved=False, created_by=self.user)
        url = reverse('stockalert-resolve', args=[alert.id])
        response = self.client.post(url, {'notes': 'Resolved by test'}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        alert.refresh_from_db()
        self.assertTrue(alert.is_resolved)