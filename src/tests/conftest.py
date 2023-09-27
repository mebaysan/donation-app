"""Defines fixtures available to all tests (Dependency Injection)."""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.management.models import Country, StateProvince

User = get_user_model()


@pytest.fixture
def client():
    """Return a new APIClient instance."""
    return APIClient()


@pytest.fixture
def country():
    """Return a new Country instance."""
    return Country.objects.create(
        name="Turkey",
        country_code="TR",
        country_code_alpha3="TUR",
        phone="+90",
        currency="TRY",
    )


@pytest.fixture
def state():
    """Return a new StateProvince instance."""
    return StateProvince.objects.create(name="Istanbul", country=country)


@pytest.fixture
def user():
    """Return a new User instance."""
    new_user = User.objects.create(
        username="testuser@email.com",
        email="testuser@email.com",
        first_name="Test",
        last_name="User",
        phone_number="+905555555555",
        gender="Male",
        is_approved_to_be_in_touch=True,
    )

    new_user.set_password("testpass123")
    new_user.save()
    return new_user
