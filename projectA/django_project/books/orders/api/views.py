from rest_framework import viewsets
from books.orders.models import OrderItem

from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = OrderItem.objects.all()
