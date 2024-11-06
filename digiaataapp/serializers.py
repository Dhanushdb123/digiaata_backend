from rest_framework import serializers
from .models import *

class ValidMobileNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValidMobileNumber
        fields = '__all__'





class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'hotel_image']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.price

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'address', 'total_amount', 'status', 'created_at', 'items']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'order', 'amount', 'payment_method', 'transaction_id', 'status', 'created_at']