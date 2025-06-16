import pytest
from core.models import Plan
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    plan = Plan.objects.create(
        name="Silver",
        max_active_charges=3,
        allowed_channels=["email", "sms"],
        weekly_charge_limit=1,
        priority_support=True,
        allow_installments=True,
    )
    user = User.objects.create_user(
        cpf="12345678900", email="user@example.com", password="strongpass123", plan=plan
    )
    return user


@pytest.fixture
def auth_client(api_client, user):
    login_response = api_client.post(
        "/auth/token/login/", data={"cpf": user.cpf, "password": "strongpass123"}
    )
    token = login_response.data.get("auth_token")
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
    return api_client


@pytest.fixture
def plan(db):
    plan, created = Plan.objects.get_or_create(
        name="Silver",
        defaults={
            "max_active_charges": 3,
            "allowed_channels": ["email", "sms"],
            "weekly_charge_limit": 1,
            "priority_support": True,
            "allow_installments": True,
        },
    )
    return plan
