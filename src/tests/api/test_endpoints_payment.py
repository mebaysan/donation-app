"""Test endpoints for payment app."""
import pytest


@pytest.mark.django_db
def test_cart_add_donation_dynamic(client, user, user_cart, donation_item_dynamic):
    """Test cart add dynamic donation."""
    client.force_authenticate(user=user)
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_dynamic.id,
            "amount": 100,
        },
    )
    assert response.status_code == 201
    assert response.json()["amount"] == "100.00"
    assert response.json()["donation_item"] == 1


@pytest.mark.django_db
def test_cart_add_donation_unauthenticated_user_fail(
    client, user, user_cart, donation_item_dynamic
):
    """Test cart add dynamic donation fail with unauthenticated user."""
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_dynamic.id,
            "amount": 100,
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_cart_add_donation_static(client, user, user_cart, donation_item_static):
    """Test cart add static donation."""
    client.force_authenticate(user=user)
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_static.id,
            "amount": 25.0,
        },
    )
    assert response.status_code == 201
    assert response.json()["amount"] == "25.00"
    assert response.json()["donation_item"] == donation_item_static.id


@pytest.mark.django_db
def test_cart_add_donation_static_fail(client, user, user_cart, donation_item_static):
    """Test cart add static donation fail. It has to be multiple of quantity price."""
    client.force_authenticate(user=user)
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_static.id,
            "amount": 26.0,
        },
    )
    assert response.status_code == 400
