"""Defines fixtures available to all tests (Dependency Injection)."""
import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient
from apps.management.models import Country, StateProvince

User = get_user_model()


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Load countries and states."""
    with django_db_blocker.unblock():
        call_command("load_countries_states")


@pytest.fixture
def client():
    """Return a new APIClient instance."""
    return APIClient()


@pytest.fixture
def country():
    """Return a new Country instance."""
    return Country.objects.filter(name="Turkey").first()


@pytest.fixture
def state():
    """Return a new StateProvince instance."""
    return StateProvince.objects.filter(name="Istanbul", country=country).first()


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


@pytest.fixture
def user2():
    """Return a new User instance."""
    new_user = User.objects.create(
        username="testuserfemale@email.com",
        email="testuserfemale@email.com",
        first_name="Test",
        last_name="User",
        phone_number="+905555555666",
        gender="Female",
        is_approved_to_be_in_touch=False,
    )

    new_user.set_password("testpass123")
    new_user.save()
    return new_user
