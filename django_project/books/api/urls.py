from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookViewSet, CategoryViewSet, GEtTokenPAirView

router = DefaultRouter()

router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'books', BookViewSet, basename='book')

app_name = 'books_api'

urlpatterns = [
    path('', include(router.urls)),
    path('get-token/', GEtTokenPAirView.as_view(), name='jwt_token'),
]
