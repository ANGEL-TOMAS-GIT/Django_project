from rest_framework import serializers
from books.orders.models import OrderItem


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"
