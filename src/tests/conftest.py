"""Defines fixtures available to all tests (Dependency Injection)."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient
from apps.management.models import Country, StateProvince, BillAddress
from apps.donor.models import DonationCategory, DonationItem, Bank, BankAccount

User = get_user_model()


@pytest.fixture()
def django_db_setup(mocker, django_db_setup, django_db_blocker):
    """Load countries and states."""
    mocker.patch(
        "apps.management.management.commands.load_countries_states.Command.get_country_state_data_from_file",
        return_value=[
            {
                "name": "Turkey",
                "countryCode": "TR",
                "countryCodeAlpha3": "TUR",
                "phone": "90",
                "currency": "TRY",
                "stateProvinces": [
                    {"name": "Istanbul"},
                    {"name": "Ankara"},
                ],
            }
        ],
    )
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
def state(country):
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


@pytest.fixture
def donation_category():
    """Return a new DonationCategory instance."""
    return DonationCategory.objects.create(
        name="Test Donation Category",
        description="Test Donation Category Description",
        order=1,
        is_published=True,
    )


@pytest.fixture
def donation_item_dynamic(donation_category):
    """Return a new dynamic DonationItem instance."""
    return DonationItem.objects.create(
        name="Test Donation Item Dynamic",
        description="Test Donation Item Dynamic Description",
        category=donation_category,
        is_published=True,
        donation_type="Dynamic",
    )


@pytest.fixture
def donation_item_static(donation_category):
    """Return a new static DonationItem instance."""
    return DonationItem.objects.create(
        name="Test Donation Item Static",
        description="Test Donation Item Static Description",
        category=donation_category,
        is_published=True,
        donation_type="Static",
        quantity_price=25.0,
    )


@pytest.fixture
def bank():
    """Return a new Bank instance."""
    return Bank.objects.create(
        name="Test Bank",
        order=1,
        is_published=True,
    )


@pytest.fixture
def bank_account(bank):
    """Return a new BankAccount instance."""
    return BankAccount.objects.create(
        bank=bank,
        account_name="Test Bank Account Name",
        description="Test Bank Account Description",
        account_number="00000",
        currency="TRY",
        swift_no="00000",
        iban_no="00000",
        branch="Test Bank Account Branch",
        branch_no="00000",
    )


@pytest.fixture
def user_cart(user):
    """Return a new Cart instance."""
    return user.cart


@pytest.fixture
def user_bill_address(user, country, state):
    """Return a new BillAddress instance."""
    return BillAddress.objects.create(
        user=user,
        address_name="Test Bill Address",
        add_line="XYZ Street. Uskudar, Istanbul, Turkiye",
        postal_code="34000",
        country=country,
        state_province=state,
    )
