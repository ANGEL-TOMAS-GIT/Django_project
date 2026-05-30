# inventory/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from inventory.models import Warehouse, ProductStock, StockMovement

User = get_user_model()


class InventoryModelTests(TestCase):
    """Tests for Inventory Models"""
    
    def setUp(self):
        self.warehouse = Warehouse.objects.create(
            name='Test Warehouse',
            location='123 Test St',
            is_active=True
        )
        
        self.product = ProductStock.objects.create(
            product_id=1,
            sku='TEST-001',
            name='Test Product',
            warehouse=self.warehouse,
            quantity=100,
            min_stock_threshold=10,
            max_stock_threshold=500
        )
    
    def test_warehouse_creation(self):
        self.assertEqual(self.warehouse.name, 'Test Warehouse')
        self.assertEqual(str(self.warehouse), 'Test Warehouse')
    
    def test_product_stock_creation(self):
        self.assertEqual(self.product.sku, 'TEST-001')
        self.assertEqual(self.product.quantity, 100)
        self.assertEqual(self.product.available_quantity, 100)
    
    def test_available_quantity_property(self):
        self.product.reserved_quantity = 30
        self.product.save()
        self.assertEqual(self.product.available_quantity, 70)
    
    def test_stock_movement_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        movement = StockMovement.objects.create(
            product_stock=self.product,
            movement_type='IN',
            quantity=50,
            notes='Test movement',
            created_by=user
        )
        
        self.assertEqual(movement.movement_type, 'IN')
        self.assertEqual(movement.quantity, 50)
        self.assertEqual(str(movement), 'IN - 50 - TEST-001')
    
    def test_low_stock_threshold(self):
        self.product.quantity = 5
        self.product.save()
        self.assertLessEqual(self.product.quantity, self.product.min_stock_threshold)


class InventoryAPITests(APITestCase):
    """Tests for Inventory API"""
    
    def setUp(self):
        # Create user and group
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # Create warehouse_manager group and add user
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
        self.warehouse = baker.make(Warehouse, is_active=True)
        self.product = baker.make(ProductStock, warehouse=self.warehouse, quantity=100)
    
    def test_list_warehouses(self):
        url = reverse('warehouse-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_warehouse(self):
        url = reverse('warehouse-list')
        data = {
            'name': 'New Warehouse',
            'location': '456 New St',
            'is_active': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Warehouse.objects.count(), 2)
    
    def test_list_stocks(self):
        url = reverse('productstock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_adjust_stock_in(self):
        url = reverse('productstock-adjust-stock', args=[self.product.id])
        data = {
            'quantity': 50,
            'movement_type': 'IN',
            'notes': 'Restocking'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 150)
    
    def test_adjust_stock_out(self):
        url = reverse('productstock-adjust-stock', args=[self.product.id])
        data = {
            'quantity': 30,
            'movement_type': 'OUT',
            'notes': 'Order fulfilled'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 70)
    
    def test_adjust_stock_insufficient(self):
        url = reverse('productstock-adjust-stock', args=[self.product.id])
        data = {
            'quantity': 200,
            'movement_type': 'OUT',
            'notes': 'Trying to overdraw'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_low_stock_filter(self):
        # Create a product with low stock
        baker.make(ProductStock, warehouse=self.warehouse, quantity=5, min_stock_threshold=10)
        
        url = reverse('productstock-low-stock')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_stock_movement_list(self):
        # Create a movement
        StockMovement.objects.create(
            product_stock=self.product,
            movement_type='IN',
            quantity=100,
            created_by=self.user
        )
        
        url = reverse('stockmovement-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)