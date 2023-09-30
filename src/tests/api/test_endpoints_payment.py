"""Test endpoints for payment app."""
import pytest
from django.contrib.auth import get_user_model
from helpers.payment_provider.payment_provider_factory import (
    PaymentProviderFactory,
    KuveytTurkPaymentProvider,
)
from django.http import HttpResponse
from apps.payment.api.serializers import (
    PaymentRequestSerializer,
    CartItemPaymentRequestSerializer,
)

User = get_user_model()


@pytest.mark.django_db
def test_new_user_has_cart(client):
    """Test new user has cart."""
    payload = {
        "phone_number": "+905555555551",
        "email": "carttestuser@email.com",
        "username": "carttestuser@email.com",
        "password": "carttestpass123",
        "confirm_new_password": "carttestpass123",
    }
    response = client.post("/api/management/users/", payload)
    user = User.objects.filter(username=payload["username"]).first()

    assert response.status_code == 201
    assert user.cart is not None


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
    assert response.json()["donation_item"] == donation_item_dynamic.id
    assert user.cart.cart_items.count() == 1
    assert user.cart.cart_items.first().donation_item == donation_item_dynamic
    assert user.cart.cart_items.first().amount == 100


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
    assert user.cart.cart_items.count() == 1
    assert user.cart.cart_items.first().donation_item == donation_item_static
    assert user.cart.cart_items.first().amount == 25.0


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


@pytest.mark.django_db
def test_cart_clean(client, user, user_cart, donation_item_static):
    """Test cart clean."""
    client.force_authenticate(user=user)
    response = client.post("/api/payment/cart/clear/")
    assert response.status_code == 200
    assert user.cart.cart_items.count() == 0


@pytest.mark.django_db
def test_cart_clean_fail_unauthenticated(client, user, user_cart, donation_item_static):
    """Test cart clean fail with unauthenticated user."""
    response = client.post("/api/payment/cart/clear/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_cart_retrieve(client, user, user_cart, donation_item_static):
    """Test cart retrieve."""
    client.force_authenticate(user=user)
    response = client.get("/api/payment/cart/")
    assert response.status_code == 200
    assert response.json()["cart_items"] == []


@pytest.mark.django_db
def test_cart_retrieve_fail_unauthenticated(
    client, user, user_cart, donation_item_static
):
    """Test cart retrieve fail with unauthenticated user."""
    response = client.get("/api/payment/cart/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_cart_update(
    client, user, user_cart, donation_item_static, donation_item_dynamic
):
    """Test cart update."""
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
    assert user.cart.cart_items.count() == 1
    assert user.cart.cart_items.first().donation_item == donation_item_static
    assert user.cart.cart_items.first().amount == 25.0

    response = client.post(
        f"/api/payment/cart/items/",
        {
            "donation_item": donation_item_dynamic.id,
            "amount": 100.0,
        },
    )
    assert response.status_code == 201
    assert user.cart.cart_items.count() == 2
    assert user.cart.amount == 125.0


@pytest.mark.django_db
def test_cart_update_fail_unauthenticated(
    client, user, user_cart, donation_item_static
):
    """Test cart update fail with unauthenticated user."""
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_static.id,
            "amount": 25.0,
        },
    )
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_published_payment_provider():
    """Test get published payment providers.
    By default we return KuveytTurkPaymentProvider
    """
    assert (
        PaymentProviderFactory.get_published_payment_provider_instance().code_name
        == "KT"
    )


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payment_provider_code_name, expected_payment_provider_class",
    [
        ("KT", KuveytTurkPaymentProvider),
        ("", KuveytTurkPaymentProvider),
        (None, KuveytTurkPaymentProvider),
    ],
)
def test_payment_provider_factory_with_different_payment_providers(
    payment_provider_code_name, expected_payment_provider_class
):
    """Test payment provider factory with different payment providers."""
    payment_provider = PaymentProviderFactory.get_payment_provider()
    assert isinstance(payment_provider, expected_payment_provider_class)


# @pytest.mark.django_db
# def test_payment_kuveytturk(
#     mocker, client, user, donation_item_dynamic, payment_provider_kuveytturk
# ):
#     """Test payment.
#     Payment data:
#     {
#         "first_name": first_name,
#         "last_name": last_name,
#         "email": email,
#         "phone_number": phone,
#         "card_number": card_number,
#         "card_holder_name": card_holder_name,
#         "card_expiry": card_expiry,
#         "card_cvc": card_cvc,
#         "message": message,
#         "donations": donations,
#         "group_name": group_name,
#         "organization_name": organization_name,
#     }
#     """
#     client.force_authenticate(user=user)
#     response = client.post(
#         "/api/payment/cart/items/",
#         {
#             "donation_item": donation_item_dynamic.id,
#             "amount": 100.0,
#         },
#     )
#     assert response.status_code == 201
#     assert response.json()["amount"] == "100.00"
#     assert response.json()["donation_item"] == donation_item_dynamic.id
#     assert user.cart.cart_items.count() == 1
#     assert user.cart.cart_items.first().donation_item == donation_item_dynamic
#     assert user.cart.cart_items.first().amount == 100.0
#
#     mocker.patch(
#         "requests.post",
#         return_value=HttpResponse(status=200),
#     )
#
#     # get payment provider payment request serializer
#     payment_request_serializer = (
#         PaymentProviderFactory.get_payment_provider_payment_request_serializer()
#     )
#
#     # create payment request serializer
#     payment_request_serializer = payment_request_serializer(
#         data={
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "phone_number": user.phone_number,
#             "card_number": "4444 2222 3333 1111",
#             "card_holder_name": "Test User",
#             "card_expiry": "12/25",
#             "card_cvc": "123",
#             "message": "Test Message",
#             "donations": [{"donation_item": donation_item_dynamic.id, "amount": 100}],
#         }
#     )
#     assert payment_request_serializer.is_valid(raise_exception=True)
#     response = client.post("/api/payment/payment/", payment_request_serializer.data)
#     print(response)
# assert response.status_code == 200
# assert response.json()["status_code"] == "00"
# assert response.json()["status_code_description"] == "Success"
# assert response.json()["md_code"] == "000000"
