from django.db import models
from django.utils import timezone
import datetime

from django.conf import settings

# Create your models here.
class ValidMobileNumber(models.Model):
    mobile_number = models.CharField(max_length=13, unique=True)
    expiration_date = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.expiration_date

    def __str__(self) -> str:
        return self.mobile_number
    


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Address(models.Model):
    name = models.CharField(max_length=100)
    address_line = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=20)
    total_billing = models.CharField(max_length=10000)

    def __str__(self):
        return self.name
    

class Order(models.Model):
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
