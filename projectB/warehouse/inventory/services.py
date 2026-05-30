# inventory/services.py
import requests
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class ProjectAClient:
    def __init__(self):
        self.base_url = settings.PROJECTA_URL
        self.timeout = 30

    def _get_token(self):
        """Get JWT token from ProjectA"""
        url = f"{self.base_url}/api/get-token/"
        data = {
            'email': settings.PROJECTA_API_USER,
            'password': settings.PROJECTA_API_PASSWORD
        }

        try:
            response = requests.post(url, json=data, verify=False, timeout=10)
            response.raise_for_status()
            token = response.json().get('access')
            if not token:
                raise Exception("No access token in response")
            return token
        except Exception as e:
            logger.error(f"Failed to get token: {str(e)}")
            raise

    def _get_headers(self):
        return {
            'X-API-Key': settings.PROJECTA_API_KEY,
            'Content-Type': 'application/json'
        }

    def check_product_stock(self, product_id):
        """Check product stock in ProjectA"""
        try:
            headers = self._get_headers()
            url = f"{self.base_url}/api/stock/{product_id}/"

            response = requests.get(url, headers=headers, verify=False, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Stock check failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Stock check error: {str(e)}")
            return None

    def reserve_stock(self, product_id, quantity, order_id):
        """Reserve stock in ProjectA"""
        try:
            headers = self._get_headers()
            url = f"{self.base_url}/api/stock/{product_id}/reserve/"
            data = {'quantity': quantity, 'order_id': order_id}

            response = requests.post(url, json=data, headers=headers, verify=False, timeout=self.timeout)

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Reserve failed: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            logger.error(f"Reserve error: {str(e)}")
            return None
