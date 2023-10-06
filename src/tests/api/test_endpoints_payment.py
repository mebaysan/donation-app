"""Test endpoints for payment app."""
import pytest
from django.contrib.auth import get_user_model
from helpers.payment.providers import KuveytTurkPaymentProvider
from helpers.payment.factory import PaymentProviderFactory
from apps.payment.models import PaymentProvider
from django.http import HttpResponse

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


@pytest.mark.django_db(transaction=True)
def test_payment(
    mocker,
    client,
    user,
    donation_item_dynamic,
):
    """
    Test payment with KuveytTurkPaymentProvider.
    """
    # set KT as payment provider
    PaymentProvider.objects.filter(code_name="KT").update(is_provider=True)

    client.force_authenticate(user=user)
    response = client.post(
        "/api/payment/cart/items/",
        {
            "donation_item": donation_item_dynamic.id,
            "amount": 100.0,
        },
    )
    assert response.status_code == 201
    assert response.json()["amount"] == "100.00"
    assert response.json()["donation_item"] == donation_item_dynamic.id
    assert user.cart.cart_items.count() == 1
    assert user.cart.cart_items.first().donation_item == donation_item_dynamic
    assert user.cart.cart_items.first().amount == 100.0

    mocker.patch(
        "requests.post",
        return_value=HttpResponse(
            status=200,
            content=b"""<!DOCTYPE html SYSTEM \'about:legacy-compat\'>\n<html class=\'no-js\' lang=\'en\' xmlns=\'http://www.w3.org/1999/xhtml\'>\n<head>\n<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\'/>\n<meta charset=\'utf-8\'/>\n<title>3D Secure Processing</title>\n</head>\n<body>\n<div id=\'main\'>\n<div id=\'content\'>\n<div id=\'order\' style=\'text-align: center;\'>\n<img src=\'https://certemvtds.bkm.com.tr/static/img/preloader.gif\' alt=\'Please wait..\'/>\n<div id=\'formdiv\'>\n<script type=\'text/javascript\'>\nfunction hideAndSubmitTimed(formid)\n{\nvar timer=setTimeout(function() {hideAndSubmit(formid)},10);\n}\n\nfunction hideAndSubmit(formid)\n{\nvar formx=document.getElementById(formid);\n\tif (formx!=null)\n\t{\n\t\tformx.style.visibility=\'hidden\';\n\t\tformx.submit();\n\t}\n}\n</script>\n<div>\n<form id=\'threeDSServerWebFlowStartForm\' name=\'threeDSServerWebFlowStartForm\' method=\'POST\' action=\'https://certemvtds.bkm.com.tr/tds/resultFlow\'>\n<input type=\'hidden\' name=\'threeDSServerWebFlowStart\' value=\'eyJhbGciOiJIUzI1NiJ9.ewogICJ0aHJlZURTU2VydmVyV2ViRmxvd1N0YXJ0IiA6IHsKICAgICJhY3F1aXJlcklEIiA6ICIyMDUiLAogICAgInRocmVlRFNTZXJ2ZXJUcmFuc0lEIiA6ICI3YjBkNzkzMi01MjNhLTQ1ODAtYTg1Zi04ODJmYWUwYzg2NWQiLAogICAgInRocmVlRFNSZXF1ZXN0b3JUcmFuc0lEIiA6ICIwMmQzMDAxYy03ZTQ3LTQ5Y2YtYTAyZi0yZDcyMDQ1YTVjOWUiLAogICAgInRpbWVab25lIiA6ICJVVEMrMDM6MDAiLAogICAgInRpbWVTdGFtcCIgOiAiMjAyMzEwMDUxNjMxNTciLAogICAgInZlcnNpb24iIDogIjEuMC4wIgogIH0KfQ.TGBStZyKRkn_FgvhmR5zz6qqIlUBAvBsEldZh5FvIf0\'/>\n<input type=\'hidden\' name=\'browserColorDepth\' value=\'\'/>\n<input type=\'hidden\' name=\'browserScreenHeight\' value=\'\'/>\n<input type=\'hidden\' name=\'browserScreenWidth\' value=\'\'/>\n<input type=\'hidden\' name=\'browserTZ\' value=\'\'/>\n<input type=\'hidden\' name=\'browserJavascriptEnabled\' value=\'\'/>\n<input type=\'hidden\' name=\'browserJavaEnabled\' value=\'\'/>\n<input type=\'hidden\' name=\'browserLanguage\' value=\'\'/>\n<script type=\'text/javascript\'>\nhideAndSubmitTimed(\'threeDSServerWebFlowStartForm\');\n</script>\n<script type=\'text/javascript\'>\nfunction collectBrowserInformation(formid)\n{\n\tvar form=document.getElementById(formid);\n\tif (form!=null)\n\t{\n\t\tif (form[\'browserJavascriptEnabled\']!=null)\n\t\t{\n\t\t\t// if this script runs js is enabled\n\t\t\tform[\'browserJavascriptEnabled\'].value="true";\n\t\t}\n\t\tif (form[\'browserJavaEnabled\']!=null)\n\t\t{\n\t\t\tform[\'browserJavaEnabled\'].value=navigator.javaEnabled();\n\t\t}\n\t\tif (form[\'browserColorDepth\']!=null)\n\t\t{\n\t\t\tform[\'browserColorDepth\'].value=screen.colorDepth;\n\t\t}\n\t\tif (form[\'browserScreenHeight\']!=null)\n\t\t{\n\t\t\tform[\'browserScreenHeight\'].value=screen.height;\n\t\t}\n\t\tif (form[\'browserScreenWidth\']!=null)\n\t\t{\n\t\t\tform[\'browserScreenWidth\'].value=screen.width;\n\t\t}\n\t\tvar timezoneOffsetField=form[\'browserTZ\'];\n\t\tif (timezoneOffsetField!=null)\n\t\t{\n\t\t\ttimezoneOffsetField.value=new Date().getTimezoneOffset();\n\t\t}\n\t\tif (form[\'browserLanguage\']!=null)\n\t\t{\n\t\t\tform[\'browserLanguage\'].value=navigator.language;\n\t\t}\n\t}\n}\ncollectBrowserInformation(\'threeDSServerWebFlowStartForm\');\n</script>\n<noscript>\n<div align=\'center\'>\n<b>Javascript is turned off or not supported!</b>\n<br/>\n</div>\n</noscript>\n<input type=\'submit\' name=\'submitBtn\' value=\'Please click here to continue\'/>\n</form>\n</div>\n</div>\n</div>\n<div id=\'content-footer\'>\n<br/>\n</div>\n</div>\n</div>\n</body>\n</html>\n""",
        ),  # we mock the response from KT
    )

    # get payment provider payment request serializer
    payment_request_serializer = (
        PaymentProviderFactory.get_payment_provider_payment_request_serializer()
    )

    # create payment request serializer
    payment_request_serializer = payment_request_serializer(
        data={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "phone_number": user.phone_number,
            "card_number": "4033 6025 6202 0327",
            "card_holder_name": "Test User",
            "card_expiry": "01/30",
            "card_cvc": "861",
            "message": "Test Message",
            "donations": [{"donation_item": donation_item_dynamic.id, "amount": 100}],
        }
    )
    assert payment_request_serializer.is_valid(raise_exception=True)
    assert payment_request_serializer.validated_data["donations"][0]["amount"] == 100

    old_user_donation_transactions_count = user.donation_transactions.count()

    response = client.post(
        "/api/payment/payment/", payment_request_serializer.data, format="json"
    )

    assert response.status_code == 200
    assert "3D Secure Processing" in response.content.decode("utf-8")
    assert (
        user.donation_transactions.count() == old_user_donation_transactions_count + 1
    )


@pytest.mark.django_db(transaction=True)
def test_payment_for_unauthenticated_new_user(
    mocker,
    client,
    donation_item_dynamic,
):
    """
    Test payment with KuveytTurkPaymentProvider for unauthenticated user.
    """
    # set KT as payment provider
    PaymentProvider.objects.filter(code_name="KT").update(is_provider=True)

    mocker.patch(
        "requests.post",
        return_value=HttpResponse(
            status=200,
            content=b"""<!DOCTYPE html SYSTEM \'about:legacy-compat\'>\n<html class=\'no-js\' lang=\'en\' xmlns=\'http://www.w3.org/1999/xhtml\'>\n<head>\n<meta http-equiv=\'Content-Type\' content=\'text/html; charset=utf-8\'/>\n<meta charset=\'utf-8\'/>\n<title>3D Secure Processing</title>\n</head>\n<body>\n<div id=\'main\'>\n<div id=\'content\'>\n<div id=\'order\' style=\'text-align: center;\'>\n<img src=\'https://certemvtds.bkm.com.tr/static/img/preloader.gif\' alt=\'Please wait..\'/>\n<div id=\'formdiv\'>\n<script type=\'text/javascript\'>\nfunction hideAndSubmitTimed(formid)\n{\nvar timer=setTimeout(function() {hideAndSubmit(formid)},10);\n}\n\nfunction hideAndSubmit(formid)\n{\nvar formx=document.getElementById(formid);\n\tif (formx!=null)\n\t{\n\t\tformx.style.visibility=\'hidden\';\n\t\tformx.submit();\n\t}\n}\n</script>\n<div>\n<form id=\'threeDSServerWebFlowStartForm\' name=\'threeDSServerWebFlowStartForm\' method=\'POST\' action=\'https://certemvtds.bkm.com.tr/tds/resultFlow\'>\n<input type=\'hidden\' name=\'threeDSServerWebFlowStart\' value=\'eyJhbGciOiJIUzI1NiJ9.ewogICJ0aHJlZURTU2VydmVyV2ViRmxvd1N0YXJ0IiA6IHsKICAgICJhY3F1aXJlcklEIiA6ICIyMDUiLAogICAgInRocmVlRFNTZXJ2ZXJUcmFuc0lEIiA6ICI3YjBkNzkzMi01MjNhLTQ1ODAtYTg1Zi04ODJmYWUwYzg2NWQiLAogICAgInRocmVlRFNSZXF1ZXN0b3JUcmFuc0lEIiA6ICIwMmQzMDAxYy03ZTQ3LTQ5Y2YtYTAyZi0yZDcyMDQ1YTVjOWUiLAogICAgInRpbWVab25lIiA6ICJVVEMrMDM6MDAiLAogICAgInRpbWVTdGFtcCIgOiAiMjAyMzEwMDUxNjMxNTciLAogICAgInZlcnNpb24iIDogIjEuMC4wIgogIH0KfQ.TGBStZyKRkn_FgvhmR5zz6qqIlUBAvBsEldZh5FvIf0\'/>\n<input type=\'hidden\' name=\'browserColorDepth\' value=\'\'/>\n<input type=\'hidden\' name=\'browserScreenHeight\' value=\'\'/>\n<input type=\'hidden\' name=\'browserScreenWidth\' value=\'\'/>\n<input type=\'hidden\' name=\'browserTZ\' value=\'\'/>\n<input type=\'hidden\' name=\'browserJavascriptEnabled\' value=\'\'/>\n<input type=\'hidden\' name=\'browserJavaEnabled\' value=\'\'/>\n<input type=\'hidden\' name=\'browserLanguage\' value=\'\'/>\n<script type=\'text/javascript\'>\nhideAndSubmitTimed(\'threeDSServerWebFlowStartForm\');\n</script>\n<script type=\'text/javascript\'>\nfunction collectBrowserInformation(formid)\n{\n\tvar form=document.getElementById(formid);\n\tif (form!=null)\n\t{\n\t\tif (form[\'browserJavascriptEnabled\']!=null)\n\t\t{\n\t\t\t// if this script runs js is enabled\n\t\t\tform[\'browserJavascriptEnabled\'].value="true";\n\t\t}\n\t\tif (form[\'browserJavaEnabled\']!=null)\n\t\t{\n\t\t\tform[\'browserJavaEnabled\'].value=navigator.javaEnabled();\n\t\t}\n\t\tif (form[\'browserColorDepth\']!=null)\n\t\t{\n\t\t\tform[\'browserColorDepth\'].value=screen.colorDepth;\n\t\t}\n\t\tif (form[\'browserScreenHeight\']!=null)\n\t\t{\n\t\t\tform[\'browserScreenHeight\'].value=screen.height;\n\t\t}\n\t\tif (form[\'browserScreenWidth\']!=null)\n\t\t{\n\t\t\tform[\'browserScreenWidth\'].value=screen.width;\n\t\t}\n\t\tvar timezoneOffsetField=form[\'browserTZ\'];\n\t\tif (timezoneOffsetField!=null)\n\t\t{\n\t\t\ttimezoneOffsetField.value=new Date().getTimezoneOffset();\n\t\t}\n\t\tif (form[\'browserLanguage\']!=null)\n\t\t{\n\t\t\tform[\'browserLanguage\'].value=navigator.language;\n\t\t}\n\t}\n}\ncollectBrowserInformation(\'threeDSServerWebFlowStartForm\');\n</script>\n<noscript>\n<div align=\'center\'>\n<b>Javascript is turned off or not supported!</b>\n<br/>\n</div>\n</noscript>\n<input type=\'submit\' name=\'submitBtn\' value=\'Please click here to continue\'/>\n</form>\n</div>\n</div>\n</div>\n<div id=\'content-footer\'>\n<br/>\n</div>\n</div>\n</div>\n</body>\n</html>\n""",
        ),  # we mock the response from KT
    )

    payload = {
        "first_name": "New User Name",
        "last_name": "New User Lastname",
        "email": "nestestuser@mail.com",
        "phone_number": "+905555555556",
        "card_number": "4033 6025 6202 0327",
        "card_holder_name": "Test User",
        "card_expiry": "01/30",
        "card_cvc": "861",
        "message": "Test Message",
        "donations": [{"donation_item": donation_item_dynamic.id, "amount": 100}],
    }

    response = client.post("/api/payment/payment/", payload, format="json")

    assert response.status_code == 200
    assert "3D Secure Processing" in response.content.decode("utf-8")

    new_user = User.objects.filter(email=payload["email"]).first()
    # check is new user created
    assert new_user is not None
    # check is new user has cart
    assert new_user.cart is not None
    # check is new user has donation
    assert (
        new_user.donation_transactions.first().donations.first().donation_item
        == donation_item_dynamic
    )
    assert new_user.donation_transactions.count() == 1
