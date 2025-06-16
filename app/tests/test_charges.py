import pytest
from core.models import Charge


@pytest.mark.django_db
def test_criar_cobranca(auth_client, user):
    data = {
        "user": user,
        "description": "Teste Cobrança",
        "total_amount": 100.0,
        "status": "Pending",
        "due_date": "2023-12-31",
        "email": "teste@teste.com",
        "phone": "21999999999",
        "whatsapp_authorized": "1",
        "installment_count": 1,
    }
    response = auth_client.post("/api/charges/", data)
    print(f"\n❌ Erro no POST /api/charges/: {response.data}")
    assert response.status_code == 201
    assert response.data["description"] == "Teste Cobrança"


@pytest.mark.django_db
def test_limite_cobrancas_ativas(auth_client, user, plan):
    # Criar as cobranças até o limite do plano
    for _ in range(plan.max_active_charges):
        Charge.objects.create(
            user=user,
            description="Cobrança",
            total_amount=50,
            status="Pending",
            due_date="2023-12-31",
            email="teste@teste.com",
            phone="21999839393",
            whatsapp_authorized=1,
            installment_count=1,
        )

    # Tentar criar uma cobrança a mais que o limite
    data = {
        "user": user,
        "description": "Extra",
        "total_amount": 60,
        "status": "Pending",
        "due_date": "2023-12-31",
        "email": "teste@teste.com",
        "phone": "21999839393",
        "whatsapp_authorized": 1,
        "installment_count": 1,
    }
    response = auth_client.post("/api/charges/", data)
    print(f"\n❌ Erro no POST /api/charges/: {response.data}")
    assert response.status_code == 400
    assert "Você atingiu o limite" in str(response.data)


@pytest.mark.django_db
def test_marcar_cobranca_como_paga(auth_client, user):
    charge = Charge.objects.create(
        user=user,
        description="Cobrança",
        total_amount=50,
        status="Pending",
        due_date="2023-12-31",
        email="teste@teste.com",
        phone="21999839393",
        whatsapp_authorized=1,
        installment_count=1,
    )
    url = f"/api/charges/{charge.id}/"
    response = auth_client.patch(url, {"status": "Paid"})
    print(f"\n❌ Erro no POST /api/charges/: {response.data}")
    assert response.status_code in (200, 204)
    charge.refresh_from_db()
    assert charge.status == "Paid"


@pytest.mark.django_db
def test_listar_cobrancas_ativas(auth_client, user):
    Charge.objects.create(
        user=user,
        description="Ativa",
        total_amount=100,
        status="Pending",
        due_date="2023-12-31",
        email="teste@teste.com",
        phone="21999839393",
        whatsapp_authorized=1,
        installment_count=1,
    )
    Charge.objects.create(
        user=user,
        description="Paga",
        total_amount=50,
        status="Paid",
        due_date="2023-12-31",
        email="teste@teste.com",
        phone="21999839393",
        whatsapp_authorized=1,
        installment_count=1,
    )
    response = auth_client.get("/api/charges/?status=Pending")
    print(f"\n❌ Erro no POST /api/charges/: {response.data}")
    assert response.status_code == 200
    assert any(c["status"] == "Pending" for c in response.data)
