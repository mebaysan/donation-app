from django.urls import path

from apps.web import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile-update/', views.profile_update, name='profile_update'),
    path('password-update/', views.password_update, name='password_update'),
    path('cart/', views.cart, name='cart'),
    path('transaction-success/', views.transaction_success, name='transaction_success'),
    path('transaction-fail/', views.transaction_fail, name='transaction_fail'),

]
