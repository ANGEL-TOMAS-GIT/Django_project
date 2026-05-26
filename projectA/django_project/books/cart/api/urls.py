from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import CartAPIView

router = DefaultRouter()

urlpatterns = [
    path("cart/", CartAPIView.as_view(), name="cart"),
]
