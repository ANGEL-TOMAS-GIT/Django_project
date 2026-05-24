from django.urls import path, include
from rest_framework.routers import DefaultRouter
from payments.views import PaymentViewSet
from payments.views import CheckoutView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

app_name = 'payments'

urlpatterns = [
    path('', include(router.urls)),
    path('checkout/<int:order_id>/', CheckoutView.as_view(), name='checkout_order')
]
