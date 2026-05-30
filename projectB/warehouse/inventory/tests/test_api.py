# inventory/tests/test_api.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from model_bakery import baker
from inventory.models import Warehouse, ProductStock

User = get_user_model()


class BaseAPITestCase(APITestCase):
    """Base class with authenticated user"""
    
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testadmin',
            email='test@test.com',
            password='testpass123',
            user_type='admin'
        )
        
        # Add user to admin group
        admin_group, _ = Group.objects.get_or_create(name='admin')
        self.user.groups.add(admin_group)
        
        # Get JWT token
        response = self.client.post('/api/auth/token/', {
            'username': 'testadmin',
            'password': 'testpass123'
        }, format='json')
        
        self.token = response.data.get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        
        # Create test data
        self.warehouse = baker.make(Warehouse, is_active=True)


class WarehouseAPITest(BaseAPITestCase):
    """Tests for Warehouse API"""
    
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


class StockAPITest(BaseAPITestCase):
    """Tests for Stock API"""
    
    def test_list_stocks(self):
        url = reverse('productstock-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_adjust_stock_in(self):
        stock = baker.make(ProductStock, warehouse=self.warehouse, quantity=100)
        url = reverse('productstock-adjust-stock', args=[stock.id])
        data = {'quantity': 50, 'movement_type': 'IN'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_adjust_stock_out(self):
        stock = baker.make(ProductStock, warehouse=self.warehouse, quantity=100)
        url = reverse('productstock-adjust-stock', args=[stock.id])
        data = {'quantity': 30, 'movement_type': 'OUT'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)