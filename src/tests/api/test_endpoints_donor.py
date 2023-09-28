"""Test endpoints for donor app."""
import pytest


@pytest.mark.django_db
def test_donation_category_list_api_view(client, donation_category):
    """Test donation category list api view."""
    response = client.get("/api/donor/categories/")

    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.django_db
def test_donation_category_detail_api_view(client, donation_category):
    """Test donation category detail api view."""
    response = client.get(f"/api/donor/categories/{donation_category.pk}/")

    assert response.status_code == 200
    assert response.json()["name"] == donation_category.name


@pytest.mark.django_db
def test_donation_item_list_api_view(
    client, donation_item_dynamic, donation_item_static
):
    """Test donation item list api view."""
    response = client.get("/api/donor/items/")

    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.django_db
def test_donation_item_detail_api_view(client, donation_item_dynamic):
    """Test donation item detail api view."""
    response = client.get(f"/api/donor/items/{donation_item_dynamic.pk}/")

    assert response.status_code == 200
    assert response.json()["name"] == donation_item_dynamic.name


@pytest.mark.django_db
def test_bank_list_api_view(client, bank, bank_account):
    """Test bank list api view."""
    response = client.get("/api/donor/banks/")

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["name"] == bank.name
    assert (
        response.json()[0]["bank_accounts"][0]["account_name"]
        == bank_account.account_name
    )
