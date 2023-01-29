from django.urls import path

from apps.payment.api import views

app_name = 'payment_api'

urlpatterns = [
    path('cart/', views.CartRetrieveAPIView.as_view(), name='cart_detail'),
]
