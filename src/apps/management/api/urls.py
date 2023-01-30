from django.urls import path

from apps.management.api import views

app_name = 'management_api'

urlpatterns = [
    path('users/me/', views.UserMeView.as_view(), name='user_details'),
    path('users/me/password-change/', views.PasswordChangeView.as_view(), name='user_password_change'),
    path('users/', views.UserCreateAPIView.as_view(), name='user_create'),
]
