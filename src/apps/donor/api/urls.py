from django.urls import path

from apps.donor.api import views

app_name = 'donor_api'

urlpatterns = [
    path('categories/', views.DonationCategoryListAPIView.as_view(), name='categories'),
    path('categories/<int:pk>/', views.DonationCategoryRetrieveAPIView.as_view(), name='category_detail'),
    path('items/', views.DonationItemListAPIView.as_view(), name='items'),
    path('items/<int:pk>/', views.DonationItemRetrieveAPIView.as_view(), name='item_detail'),
    path('banks/', views.BankListAPIView.as_view(), name='banks'),

]
