import logging

from celery import shared_task
from django.core.mail import send_mail

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
    from .utils import send_whatsapp_message

    sid = send_whatsapp_message(phone, variables_dict)
    logger.info(f"WhatsApp enviado para {phone} com SID {sid}")
    return f"WhatsApp enviado para {phone} com SID {sid}"


@shared_task
def enviar_lembretes_diarios_task():
    from .utils import enviar_lembretes_diarios

    print("Iniciando envio de lembretes diários...")
    enviar_lembretes_diarios()
