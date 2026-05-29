from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, GEtTokenPAirView, CheckStockView, ReserveStockView

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'books', BookViewSet, basename='book')

app_name = 'books_api'

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', GEtTokenPAirView.as_view(), name='jwt_token'),
    path('stock/<int:product_id>/', CheckStockView.as_view(), name='check_stock'),
    path('stock/<int:product_id>/reserve/', ReserveStockView.as_view(), name='reserve_stock'),
]
