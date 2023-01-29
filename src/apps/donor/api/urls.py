from django.urls import path

from apps.donor.api import views

app_name = 'donor_api'

urlpatterns = [
    path('categories/', views.DonationCategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.DonationCategoryRetrieveAPIView.as_view(), name='category_detail'),
    path('items/', views.DonationItemListAPIView.as_view(), name='items'),
    path('items/<int:pk>/', views.DonationItemRetrieveAPIView.as_view(), name='item_detail'),
    path('donations/', views.DonationListAPIView.as_view(), name='donations'),
    path('transactions/', views.DonationTransactionListAPIView.as_view(), name='transactions'),
    path('transactions/<int:pk>/', views.DonationTransactionRetrieveAPIView.as_view(), name='transaction_details'),
]
