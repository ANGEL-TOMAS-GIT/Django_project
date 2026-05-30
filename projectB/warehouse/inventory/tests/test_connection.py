# inventory/tests/test_connection.py
from django.test import TestCase
from unittest.mock import patch, MagicMock
from inventory.services import ProjectAClient


class ConnectionTest(TestCase):
    """Test connection between ProjectB and ProjectA using mocks"""

    def setUp(self):
        self.client = ProjectAClient()

    @patch('inventory.services.requests.get')
    def test_check_stock_returns_data(self, mock_get):
        """Test that check_product_stock returns data (mocked)"""
        # Create mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'product_id': 1,
            'sku': 'BOOK-1',
            'name': 'Test Book',
            'available_quantity': 30,
            'status': 'available'
        }
        mock_get.return_value = mock_response

        result = self.client.check_product_stock(1)

        self.assertIsNotNone(result)
        self.assertEqual(result['product_id'], 1)
        self.assertEqual(result['available_quantity'], 30)

        # Verify the API was called correctly
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertIn('/api/stock/1/', args[0])

        print("✅ check_product_stock test passed")

    @patch('inventory.services.requests.post')
    def test_reserve_stock_returns_response(self, mock_post):
        """Test that reserve_stock returns a response (mocked)"""
        # Create mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'success': True,
            'product_id': 1,
            'reserved_quantity': 1,
            'remaining_stock': 29,
            'order_id': 9999
        }
        mock_post.return_value = mock_response

        result = self.client.reserve_stock(1, 1, 9999)

        self.assertIsNotNone(result)
        self.assertTrue(result['success'])
        self.assertEqual(result['reserved_quantity'], 1)

        # Verify the API was called correctly
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('/api/stock/1/reserve/', args[0])
        self.assertEqual(kwargs['json']['quantity'], 1)
        print("✅ reserve_stock test passed")
    
    @patch('inventory.services.requests.get')
    def test_check_stock_handles_error(self, mock_get):
        """Test that check_stock handles errors gracefully"""
        # Mock an error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response
        result = self.client.check_product_stock(1)
        self.assertIsNone(result)
        print("✅ Error handling test passed")

    @patch('inventory.services.requests.post')
    def test_reserve_stock_handles_error(self, mock_post):
        """Test that reserve_stock handles errors gracefully"""
        # Mock an error response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        result = self.client.reserve_stock(1, 1, 9999)
        self.assertIsNone(result)
        print("✅ Error handling test passed")