"""Tests for the management app API."""

import pytest
from apps.management.models import Country, StateProvince


def test_endpoint_healthcheck(client):
    """Tests the healthcheck endpoint."""
    response = client.get("/api/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_endpoint_generate_password(client):
    """Tests the generate password endpoint."""
    response = client.get("/api/management/generate-password/")
    assert response.status_code == 200
    assert response.json().get("password") is not None


@pytest.mark.django_db
def test_register_user(client):
    """Tests the register user endpoint."""
    payload = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "test@baysansoft.com",
        "password": "testpass1233123123",
        "confirm_new_password": "testpass1233123123",
    }
    response = client.post("/api/management/users/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_register_user_fail_invalid_username(client):
    """Tests the register user endpoint with invalid username"""
    payload = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "notequal@baysansoft.com",
        "password": "testpass1233123123",
        "confirm_new_password": "testpass1233123123",
    }
    response = client.post("/api/management/users/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_fail_invalid_password(client):
    """Tests the register user endpoint with invalid password."""
    payload = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "test@baysansoft.com",
        "password": "testpass123",
        "confirm_new_password": "testpass1233123123",
    }
    response = client.post("/api/management/users/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_fail_already_registered_email(client):
    """Tests the register user endpoint for already registered user."""
    payload = {
        "phone_number": "+905555555555",
        "email": "testuser@email.com",
        "username": "testuser@email.com",
        "password": "testpass123",
        "confirm_new_password": "testpass123",
    }
    response = client.post("/api/management/users/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_register_user_fail_already_registered_phone_number(client):
    """Tests the register user endpoint
    for already registered user with phone_number.
    """
    payload = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "test@baysansoft.com",
        "password": "testpass123",
        "confirm_new_password": "testpass123",
    }
    response = client.post("/api/management/users/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_login_user_with_email(client, user):
    """Tests the login user endpoint with email."""
    payload = {
        "username": user.username,
        "password": "testpass123",
    }
    response = client.post("/api/token/", payload)

    assert response.status_code == 200
    assert response.json().get("token") is not None


@pytest.mark.django_db
def test_login_user_with_phone_number(client, user):
    """Tests the login user endpoint with phone_number."""
    payload = {
        "username": user.phone_number,
        "password": "testpass123",
    }
    response = client.post("/api/token/", payload)

    assert response.status_code == 200
    assert response.json().get("token") is not None


@pytest.mark.django_db
def test_login_user_fail(client, user):
    """Tests the login user endpoint."""
    # Test with invalid password
    payload = {
        "username": user.username,
        "password": "testpass1233123123",
    }
    response = client.post("/api/token/", payload)

    assert response.status_code == 401


@pytest.mark.django_db
def test_user_me(client, user):
    """Tests the user me endpoint."""
    client.force_authenticate(user=user)
    response = client.get("/api/management/users/me/")
    assert response.status_code == 200
    assert response.json().get("id") == user.id
    assert response.json().get("username") == user.username
    assert response.json().get("email") == user.email
    assert response.json().get("phone_number") == user.phone_number
    assert response.json().get("first_name") == user.first_name
    assert response.json().get("last_name") == user.last_name
    assert response.json().get("country") == user.country
    assert response.json().get("state_province") == user.state_province


@pytest.mark.django_db
def test_user_me_fail(client):
    """Tests the user me endpoint."""
    response = client.get("/api/management/users/me/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_me_update_user(client, user):
    """Tests the user me endpoint to update the user's information."""
    client.force_authenticate(user=user)

    payload = {
        "phone_number": "+905555555556",
        "first_name": "Test Updated",
        "last_name": "User Updated",
        "username": "testuser2@email.com",
        "email": "testuser2@email.com",
    }
    response = client.patch("/api/management/users/me/", payload)

    assert response.status_code == 200
    assert response.json().get("phone_number") == payload.get("phone_number")
    assert response.json().get("first_name") == payload.get("first_name")
    assert response.json().get("last_name") == payload.get("last_name")
    assert response.json().get("username") == payload.get("username")
    assert response.json().get("email") == payload.get("username")
    assert response.json().get("username") == payload.get("email")
    assert response.json().get("email") == payload.get("email")


@pytest.mark.django_db
def test_user_me_update_user_fail_with_wrong_credentials(client, user):
    """Tests the user me endpoint to update the user's information.
    with invalid payload. email != username
    """
    client.force_authenticate(user=user)

    payload = {
        "phone_number": "+905555555556",
        "first_name": "Test Updated",
        "last_name": "User Updated",
        "username": "testuser2@email.com",
        "email": "testuser@email.com",
    }
    response = client.patch("/api/management/users/me/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_user_me_update_user_fail_already_created(client, user, user2):
    """Tests the user me endpoint to update the user's information.
    with existing user's credentials.
    We are trying to update user2 with user's credentials.
    """
    client.force_authenticate(user=user2)

    payload = {
        "phone_number": user.phone_number,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email": user.email,
    }
    response = client.patch("/api/management/users/me/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_change_password(client, user):
    """Tests the change password endpoint."""
    client.force_authenticate(user=user)

    payload = {
        "old_password": "testpass123",
        "new_password": "testpass1234!.",
        "confirm_new_password": "testpass1234!.",
    }
    response = client.patch("/api/management/users/me/password-change/", payload)

    assert response.status_code == 200


@pytest.mark.django_db
def test_user_change_password_fail(client, user):
    """Tests the change password endpoint fail."""
    client.force_authenticate(user=user)

    payload = {
        "old_password": "testpass",
        "new_password": "testpass1234!.",
        "confirm_new_password": "testpass1234!.",
    }
    response = client.patch("/api/management/users/me/password-change/", payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_forgot_password_with_email(client, user):
    """Tests the forgot password endpoint with username, email."""
    # Forgot password
    payload_forgot = {
        "username": user.email,
    }
    response_forgot = client.post("/api/management/forgot-password/", payload_forgot)

    # User can not login with old password
    payload_login = {
        "username": user.email,
        "password": "testpass123",
    }
    response_login = client.post("/api/token/", payload_login)

    assert response_forgot.status_code == 200
    assert response_login.status_code == 401


@pytest.mark.django_db
def test_user_forgot_password_with_phone_number(client, user):
    """Tests the forgot password endpoint with phone_number."""
    # Forgot password
    payload_forgot = {
        "username": user.phone_number,
    }
    response_forgot = client.post("/api/management/forgot-password/", payload_forgot)

    # User can not login with old password
    payload_login = {
        "username": user.phone_number,
        "password": "testpass123",
    }
    response_login = client.post("/api/token/", payload_login)

    assert response_forgot.status_code == 200
    assert response_login.status_code == 401


@pytest.mark.django_db
def test_user_forgot_password_fail(client):
    """Tests the forgot password endpoint fail."""
    payload = {
        "username": "not_exist_user@test.com",
    }
    response = client.post("/api/management/forgot-password/", payload)
    assert response.status_code == 400


@pytest.mark.django_db
def test_country_list(client):
    """Tests the country list endpoint."""
    response = client.get("/api/management/countries/")
    assert response.status_code == 200
    assert len(response.json()) == Country.objects.count()


@pytest.mark.django_db
def test_country_details(client, country):
    """Tests the country details endpoint."""
    response = client.get(f"/api/management/countries/{country.id}/")
    assert response.status_code == 200
    assert response.json().get("id") == country.id
    assert response.json().get("name") == country.name
    assert response.json().get("country_code") == country.country_code
    assert response.json().get("country_code_alpha3") == country.country_code_alpha3
    assert response.json().get("phone") == country.phone
    assert response.json().get("currency") == country.currency


@pytest.mark.django_db
def test_bill_address_list(client, user, user_bill_address):
    """Tests the bill address list endpoint."""
    client.force_authenticate(user)
    response = client.get("/api/management/bill-address/")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_bill_address_create(client, user, country, state):
    """Tests the bill address create endpoint."""
    client.force_authenticate(user)

    payload = {
        "address_name": "Home address for test purposes",
        "add_line": "Uskudar Istanbul",
        "postal_code": "340000",
        "state_province": state.id,
        "country": country.id,
    }
    response = client.post("/api/management/bill-address/", payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_bill_address_delete(client, user, user_bill_address):
    """Tests the bill address delete endpoint."""
    client.force_authenticate(user)
    response = client.delete(f"/api/management/bill-address/{user_bill_address.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_bill_address_update(client, user, user_bill_address):
    """Tests the bill address update endpoint."""
    client.force_authenticate(user)

    payload = {
        "address_name": "Home address for test purposes UPDATED",
        "add_line": "Uskudar Istanbul",
        "postal_code": "340000",
        "state_province": user_bill_address.state_province.id,
        "country": user_bill_address.country.id,
    }
    response = client.patch(
        f"/api/management/bill-address/{user_bill_address.id}/", payload
    )
    assert response.status_code == 200
    assert response.json().get("address_name") == payload.get("address_name")
    assert response.json().get("add_line") == payload.get("add_line")
    assert response.json().get("postal_code") == payload.get("postal_code")
    assert response.json().get("state_province") == payload.get("state_province")


@pytest.fixture
def test_bill_address_get(client, user, user_bill_address):
    """Tests the bill address get endpoint."""
    client.force_authenticate(user)
    response = client.get(f"/api/management/bill-address/{user_bill_address.id}/")
    assert response.status_code == 200
    assert response.json().get("address_name") == user_bill_address.address_name
    assert response.json().get("add_line") == user_bill_address.add_line
    assert response.json().get("postal_code") == user_bill_address.postal_code
    assert response.json().get("state_province") == user_bill_address.state_province.id
    assert response.json().get("country") == user_bill_address.country.id
