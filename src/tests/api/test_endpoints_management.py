"""Tests for the management app API."""
import pytest


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
    """Tests the register user endpoint for already registered user with phone_number."""
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
