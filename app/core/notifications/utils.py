import json
import os

from core.models import Charge
from twilio.rest import Client

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def send_whatsapp_message(
    to, variables_dict, content_sid="HX57392078ee0971d48ed095d683e71507"
):
    print(f"Enviando WhatsApp para {to} com variáveis {variables_dict}")
    message = client.messages.create(
        from_=TWILIO_WHATSAPP_FROM,
        content_sid=content_sid,
        content_variables=json.dumps(variables_dict),
        to=f"whatsapp:{to}",
    )
    return message.sid


def enviar_lembretes_diarios():
    from .tasks import send_email_task, send_whatsapp_task

    # pega as cobranças vencendo hoje e que ainda não foram pagas
    dividas = Charge.objects.filter(status="Pending")
    print(f"Encontradas {dividas.count()} cobranças pendentes para enviar lembretes.")
    for divida in dividas:
        cobrador = divida.user  # o usuário que criou a cobrança
        devedor_nome = divida.name  # ou o campo que representa o nome do cliente
        valor = divida.total_amount

        # prepara mensagem pro zap (as variáveis que o template espera)
        variaveis = {
            "1": cobrador.name or cobrador.username,
            "2": devedor_nome,
            "3": f"{valor:.2f}",
            "4": divida.description,
        }

        # dispara a task do zap assincronamente

        if divida.phone == "21999839393":
            print(f"Enviando WhatsApp para {divida.phone} com variáveis {variaveis}")
            send_whatsapp_task.delay(
                phone=divida.phone,
                variables_dict=variaveis,
            )

        # dispara a task do email
        assunto = "Lembrete de dívida pendente"
        texto_email = f"""
        Sr.(a) {variaveis['1']},

        Lembramos que tem uma dívida em aberto com o Sr.(a) {variaveis['2']}, no valor de
        R$ {variaveis['3']}. Referente à dívida: {variaveis['4']}
        Aguardamos contato com o mesmo para regularização da dívida.

        Atenciosamente,
        MicroSaaS Cobranças
        """

        send_email_task.delay(
            to_email=cobrador.email,
            subject=assunto,
            message=texto_email,
        )
