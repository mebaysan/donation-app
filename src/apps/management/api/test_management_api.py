"""Tests for the management app API."""
import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_endpoint_healthcheck():
    """Tests the healthcheck endpoint."""
    response = client.get("/api/healthcheck/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
