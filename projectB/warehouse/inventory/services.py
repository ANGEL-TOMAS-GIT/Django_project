import requests
import logging
from django.conf import settings
from django.core.cache import cache
from rest_framework import status

logger = logging.getLogger(__name__)


class ProjectAClient:
    """Client for communicating with ProjectA API"""
    
    def __init__(self):
        self.base_url = settings.PROJECTA_URL
        self.timeout = 30
    
    def _get_headers(self):
        token = cache.get('projecta_token')
        if not token:
            token = self._refresh_token()
        return {'Authorization': f'Bearer {token}'}
    
    def _refresh_token(self):
        try:
            response = requests.post(
                f"{self.base_url}/api/token/",
                json={
                    'username': settings.PROJECTA_API_USER,
                    'password': settings.PROJECTA_API_PASSWORD
                },
                timeout=10
            )
            response.raise_for_status()
            token = response.json()['access']
            cache.set('projecta_token', token, 3600)
            return token
        except requests.RequestException as e:
            logger.error(f"Failed to refresh token: {str(e)}")
            raise
    
    def verify_order(self, order_id):
        """Verify order exists in ProjectA"""
        try:
            response = requests.get(
                f"{self.base_url}/api/orders/{order_id}/",
                headers=self._get_headers(),
                timeout=self.timeout
            )
            
            if response.status_code == status.HTTP_200_OK:
                return response.json()
            elif response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            else:
                response.raise_for_status()
        except requests.RequestException as e:
            logger.error(f"Order verification error: {str(e)}")
            raise
    
    def update_order_status(self, order_id, status, notes=None):
        """Update order status in ProjectA"""
        try:
            payload = {'warehouse_status': status}
            if notes:
                payload['warehouse_notes'] = notes
            
            response = requests.patch(
                f"{self.base_url}/api/orders/{order_id}/",
                json=payload,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Order status update error: {str(e)}")
            raise
