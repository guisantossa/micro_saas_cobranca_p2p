import pytest


@pytest.mark.django_db
def test_login_sucesso(api_client, user):
    response = api_client.post(
        "/auth/token/login/", data={"cpf": user.cpf, "password": "strongpass123"}
    )
    assert response.status_code == 200
    assert "auth_token" in response.data


@pytest.mark.django_db
def test_login_senha_errada(api_client, user):
    response = api_client.post(
        "/auth/token/login/", data={"cpf": user.cpf, "password": "errada"}
    )
    assert response.status_code == 400
    assert "Unable to log in with provided credentials." in str(response.data)


@pytest.mark.django_db
def test_login_cpf_inexistente(api_client):
    response = api_client.post(
        "/auth/token/login/", data={"cpf": "00000000000", "password": "qualquer"}
    )
    assert response.status_code == 400
    assert "Unable to log in with provided credentials." in str(response.data)
