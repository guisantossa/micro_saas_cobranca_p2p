import requests
from django.conf import settings
from users.models import UserBankSettings

ASAAS_API_KEY = settings.ASAAS_API_KEY
ASAAS_BASE_URL = settings.ASAAS_BASE_URL

HEADERS = {
    "Content-Type": "application/json",
    "access_token": ASAAS_API_KEY,
}


def create_or_update_recipient(user, bank_data: UserBankSettings):
    payload = {
        "bankCode": bank_data.bank_code,
        "agency": bank_data.agency,
        "account": bank_data.account,
        "accountDigit": bank_data.account_digit,
        "accountType": bank_data.account_type,
        "cpfCnpj": user.cpf,  # assume que o CPF está no seu user model
        "name": user.name,
        "email": user.email,
        "mobilePhone": user.phone,
        "address": user.address,
        "incomeValue": 100,  # Valor de renda, se necessário
        "addressNumber": user.address_number,
        "province": user.state,
        "postalCode": user.zipcode,
        "birthDate": user.birth_date.isoformat(),
    }
    if bank_data.asaas_recipient_id:
        url = f"{ASAAS_BASE_URL}/accounts/{bank_data.asaas_recipient_id}"
        response = requests.put(url, json=payload, headers=HEADERS)
    else:
        url = f"{ASAAS_BASE_URL}/accounts"
        response = requests.post(url, json=payload, headers=HEADERS)

    if response.status_code not in [200, 201]:
        print(
            "Erro ao criar/atualizar conta de transferência:",
            response.status_code,
            response.text,
        )
        return None

    data = response.json()
    return data.get("id")
