from django.urls import path

from apps.management.api import views

app_name = "management_api"

urlpatterns = [
    path("users/me/", views.UserMeView.as_view(), name="user_details"),
    path(
        "generate-password/",
        views.GeneratePasswordView.as_view(),
        name="generate_password",
    ),
    path(
        "users/me/password-change/",
        views.PasswordChangeView.as_view(),
        name="user_password_change",
    ),
    path("users/", views.UserCreateAPIView.as_view(), name="user_create"),
    path(
        "forgot-password/",
        views.ForgotPasswordAPIView.as_view(),
        name="forgot_password",
    ),
    path("countries/", views.CountryListAPIView.as_view(), name="country_list"),
    path(
        "countries/<int:id>/",
        views.CountryDetailsAPIView.as_view(),
        name="country_detail",
    ),
    path(
        "bill-address/",
        views.BillAddressListCreateAPIView.as_view(),
        name="bill_address_list",
    ),
    path(
        "bill-address/<int:id>/",
        views.BillAddressRetrieveUpdateDestroyAPIView.as_view(),
        name="bill_address_details",
    ),
]
