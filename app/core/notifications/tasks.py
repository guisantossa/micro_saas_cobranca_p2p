import logging

import requests
from celery import shared_task
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_email_task(to_email, subject, message):
    print(f"Enviando email para {to_email} com assunto '{subject}'")
    send_mail(
        subject,
        message,
        "no-reply@cobraii.com.br",  # ajusta esse
        [to_email],
        fail_silently=False,
    )
    return f"Email enviado para {to_email}"


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_whatsapp_task(phone, variables_dict):
    logger.info(
        f"Enviando WhatsApp via n8n para {phone} com variáveis {variables_dict}"
    )
    payload = {
        "numero": f"55{phone}",
        "nome": variables_dict.get("nome"),
        "valor": variables_dict.get("valor"),
        "autor": variables_dict.get("autor"),
        "url": variables_dict.get("url"),
        "descricao": variables_dict.get("descricao"),
    }
    try:
        response = requests.post(
            "https://n8n.zapgastos.com.br/webhook/cobraii-cobranca",
            json=payload,
            headers={"Content-Type": "application/json"},
        )
        response.raise_for_status()
        logger.info(f"Mensagem enviada com sucesso: {response.status_code}")
        return f"Mensagem enviada com sucesso para {phone}"
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar WhatsApp: {str(e)}")
        return f"Erro ao enviar mensagem para {phone}: {str(e)}"


@shared_task
def enviar_lembretes_diarios_task():
    from .utils import enviar_lembretes_diarios

    print("Iniciando envio de lembretes diários...")
    enviar_lembretes_diarios()
