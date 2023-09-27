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
def test_register_user_fail(client):
    """Tests the register user endpoint."""
    # Test with invalid username (email and username must be equal)
    payload1 = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "notequal@baysansoft.com",
        "password": "testpass1233123123",
        "confirm_new_password": "testpass1233123123",
    }
    response1 = client.post("/api/management/users/", payload1)

    # Test with invalid password
    # (password and confirm_new_password must be equal)
    payload2 = {
        "phone_number": "+905555555555",
        "email": "test@baysansoft.com",
        "username": "test@baysansoft.com",
        "password": "testpass123",
        "confirm_new_password": "testpass1233123123",
    }
    response2 = client.post("/api/management/users/", payload2)

    assert response1.status_code == 400
    assert response2.status_code == 400
