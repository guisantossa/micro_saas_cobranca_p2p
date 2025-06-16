import pytest
from users.models import User


@pytest.mark.django_db
def test_criar_cliente_valido():
    user = User.objects.create_user(
        cpf="98765432100", email="novo@exemplo.com", password="senha123"
    )
    assert user.cpf == "98765432100"
    assert user.email == "novo@exemplo.com"
    assert user.check_password("senha123")


@pytest.mark.django_db
def test_editar_cliente_sem_senha(auth_client, user):
    url = f"/auth/users/{user.id}/"
    data = {"email": "editado@exemplo.com"}
    response = auth_client.patch(url, data)
    assert response.status_code in (200, 204)
    user.refresh_from_db()
    assert user.email == "editado@exemplo.com"


@pytest.mark.django_db
def test_cpf_duplicado():
    User.objects.create_user(
        cpf="11122233344", email="primeiro@ex.com", password="senha"
    )
    with pytest.raises(Exception):
        User.objects.create_user(
            cpf="11122233344", email="segundo@ex.com", password="senha"
        )


@pytest.mark.django_db
def test_listar_clientes(auth_client):
    response = auth_client.get("/auth/users/")
    assert response.status_code == 200
    assert isinstance(response.data, list)
