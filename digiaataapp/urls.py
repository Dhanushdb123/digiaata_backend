from django.urls import path

from digiaataapp import views


urlpatterns = [
    #login urls.py
    path('login', views.enter_mobile_number, name='enter_mobile_number'),

    # Product URLs
    path('products/', views.product_list, name='product-list'),
    path('cart/add/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.view_cart, name='view-cart'),
    path('addresses/', views.address_list, name='address-list'),
    path('order/create/', views.create_order, name='create-order'),
    path('payment/process/', views.process_payment, name='process-payment'),


]