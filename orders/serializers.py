from rest_framework import serializers
from .models import Order, OrderItem
from pharmacy.models import Drug

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'drug', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = ['id', 'user', 'total_price', 'address', 'city', 'postal_code', 'country', 'payment_method', 'status', 'created_at', 'updated_at', 'items']
