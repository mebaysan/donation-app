from django.urls import path

from apps.payment.api import views

app_name = 'payment_api'

urlpatterns = [
    path('cart/', views.CartRetrieveAPIView.as_view(), name='cart_details'),
    path('cart/items/', views.CartItemCreateAPIView.as_view(), name='cart_item_add'),
    path('cart/items/<int:pk>/', views.CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cart_item_details'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('payment-fail/', views.payment_fail, name='payment_fail'),
]
