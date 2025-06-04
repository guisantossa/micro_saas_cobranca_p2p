import json
import logging
import os

from celery import shared_task
from django.core.mail import send_mail
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_CONTENT_SID = os.getenv("TWILIO_CONTENT_SID")
if not all(
    [TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM, TWILIO_CONTENT_SID]
):
    raise ValueError("Variáveis de ambiente TWILIO faltando!")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

logger = logging.getLogger(__name__)


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_email_task(to_email, subject, message):
    print(f"Enviando email para {to_email} com assunto '{subject}'")
    send_mail(
        subject,
        message,
        "no-reply@microsaas.com",  # ajusta esse
        # [to_email],
        ["eleteasi@gmail.com"],
        fail_silently=False,
    )
    return f"Email enviado para {to_email}"


@shared_task(autoretry_for=(Exception,), retry_backoff=True, max_retries=3)
def send_whatsapp_task(phone, variables_dict):
    print(f"Enviando WhatsApp para {phone} com variáveis {variables_dict}")
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        content_sid=TWILIO_CONTENT_SID,
        content_variables=json.dumps(variables_dict),
        to=f"whatsapp:{phone}",
    )
    sid = message.sid
    logger.info(f"WhatsApp enviado para {phone} com SID {sid}")
    return f"WhatsApp enviado para {phone} com SID {sid}"


@shared_task
def enviar_lembretes_diarios_task():
    from .utils import enviar_lembretes_diarios

    print("Iniciando envio de lembretes diários...")
    enviar_lembretes_diarios()
