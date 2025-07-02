from datetime import date

import environ
import requests
from core.models import AsaasCustomer
from django.conf import settings  # noqa: F401

env = environ.Env()
environ.Env.read_env()

ASAAS_API_URL = env("ASAAS_BASE_URL")
# ASAAS_API_URL = "https://api-sandbox.asaas.com/v3"
ASAAS_API_KEY = "$" + env("ASAAS_API_KEY")
WALLET_ID = env("ASAAS_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "CobraiiSaaS/1.0",
    "access_token": ASAAS_API_KEY,
}


def get_or_create_asaas_customer(data):
    try:
        customer = AsaasCustomer.objects.get(cpfCnpj=data["cpfCnpj"])
        return customer.asaas_id
    except AsaasCustomer.DoesNotExist:
        # Criar no ASAAS
        payload = {
            "name": data["name"],
            "email": data["email"],
            "mobilePhone": "+55" + data["phone"],  # Formato E.164, ex: +5511999999999
            "cpfCnpj": data["cpfCnpj"],
        }
        response = requests.post(
            f"{ASAAS_API_URL}/customers", json=payload, headers=HEADERS
        )

        if response.status_code not in [200, 201]:
            try:
                error_detail = response.json()
            except Exception:
                error_detail = response.text  # fallback bruto se não for JSON

            print("❌ ERRO ASAAS:", response.status_code)
            print("📩 Payload Enviado:", payload)
            print("📨 Resposta do ASAAS:", error_detail)

        data = response.json()
        customer = AsaasCustomer.objects.create(
            nome=data["name"],
            email=data["email"],
            phone=data["mobilePhone"],
            cpfCnpj=data["cpfCnpj"],
            asaas_id=data["id"],
        )
        return customer.asaas_id


def create_asaas_charge(customer_id, charge_data, cobrador_recipient_id):
    headers = {
        "Content-Type": "application/json",
        "access_token": ASAAS_API_KEY,
    }

    payload = {
        "customer": customer_id,
        "billingType": charge_data["billingType"],  # ou "PIX", "BOLETO", "CREDIT_CARD"
        "value": float(charge_data["total_amount"]),
        "dueDate": date.today().isoformat(),  # data de vencimento
        "description": charge_data.get("description"),
        "split": [
            {
                "walletId": cobrador_recipient_id,
                "percentualValue": 95,  # ou valor percentual se preferir
            },
        ],
    }

    response = requests.post(f"{ASAAS_API_URL}/payments", json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()  # contém invoiceUrl, id etc.
    else:
        raise Exception(f"Erro ao criar cobrança no ASAAS: {response.text}")
