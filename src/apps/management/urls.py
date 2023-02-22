from django.urls import path

from apps.management import views

app_name = "management"

urlpatterns = [
    path(
        "password-reset/<uidb64>/<token>/", views.password_reset, name="password_reset"
    ),
    path("password-reset/ok/", views.password_reset_complete, name="password_reset_ok"),
]
