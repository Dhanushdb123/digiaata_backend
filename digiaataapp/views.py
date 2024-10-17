from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from rest_framework.views import APIView
# import razorpay
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *
# import uuid
# from phonepe.sdk.pg.payments.v1.models.request.pg_pay_request import PgPayRequest
# from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
# from phonepe.sdk.pg.env import Env
import json


# Create your views here.


@api_view(['POST'])
def enter_mobile_number(request):
    mobile_number = request.data.get('mobile_number')

    if not mobile_number:
        return Response({"error": "Mobile number is required"}, status=status.HTTP_400_BAD_REQUEST)

    expiration_date = timezone.now() + timedelta(weeks=1)
    valid_mobile_number, created = ValidMobileNumber.objects.get_or_create(
        mobile_number=mobile_number,
        defaults={'expiration_date': expiration_date}
    )

    if not valid_mobile_number.is_valid():
        return Response({"error": "Mobile number has expired"}, status=status.HTTP_401_UNAUTHORIZED)

    serializer = ValidMobileNumberSerializer(valid_mobile_number)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    quantity = int(request.data.get('quantity', 1))
    
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_item, created = CartItem.objects.get_or_create(product=product)
    cart_item.quantity = quantity
    cart_item.save()

    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data)

@api_view(['GET'])
def view_cart(request):
    cart_items = CartItem.objects.all()
    serializer = CartItemSerializer(cart_items, many=True)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return Response({'items': serializer.data, 'total': total})

@api_view(['GET', 'POST'])
def address_list(request):
    if request.method == 'GET':
        addresses = Address.objects.all()
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_order(request):
    address_id = request.data.get('address_id')
    
    try:
        address = Address.objects.get(id=address_id)
    except Address.DoesNotExist:
        return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

    cart_items = CartItem.objects.all()
    
    if not cart_items:
        return Response({'error': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

    total_amount = sum(item.quantity * item.product.price for item in cart_items)
    
    order = Order.objects.create(address=address, total_amount=total_amount)
    
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )

    cart_items.delete()  # Clear the cart

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



import uuid

@api_view(['POST'])
def process_payment(request):
    order_id = request.data.get('order_id')
    payment_method = request.data.get('payment_method')

    try:
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    # Check if payment already exists for this order
    if hasattr(order, 'payment'):
        return Response({'error': 'Payment already processed for this order'}, status=status.HTTP_400_BAD_REQUEST)

    # Generate a unique transaction ID
    transaction_id = str(uuid.uuid4())

    # Create a new payment
    payment = Payment.objects.create(
        order=order,
        amount=order.total_amount,
        payment_method=payment_method,
        transaction_id=transaction_id,
        status='successful'  # In a real scenario, this would depend on the payment gateway response
    )

    # Update order status
    order.status = 'paid'
    order.save()

    serializer = PaymentSerializer(payment)
    return Response({
        'message': 'Payment processed successfully',
        'payment': serializer.data
    }, status=status.HTTP_200_OK)
