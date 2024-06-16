from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    drug_name = serializers.ReadOnlyField(source='drug.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'drug', 'drug_name', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
