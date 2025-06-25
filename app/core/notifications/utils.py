from datetime import timedelta

from core.models import Charge, Notification
from django.utils import timezone


def enviar_lembretes_diarios():
    from .tasks import send_email_task, send_whatsapp_task

    hoje = timezone.now()
    uma_semana_atras = hoje - timedelta(days=7)

    # pega as cobranças vencendo hoje e que ainda não foram pagas
    dividas = Charge.objects.filter(status="Pending")
    print(f"Encontradas {dividas.count()} cobranças pendentes para enviar lembretes.")
    for divida in dividas:

        ja_foi_notificada = Notification.objects.filter(
            charge=divida,
            sent_at__gte=uma_semana_atras,
        ).exists()
        if ja_foi_notificada:
            print(f"Pulando cobrança {divida.id} (já notificada recentemente)")
            continue
        cobrador = divida.user  # o usuário que criou a cobrança
        devedor_nome = divida.name  # ou o campo que representa o nome do cliente
        valor = divida.total_amount

        # prepara mensagem pro zap (as variáveis que o template espera)
        variaveis = {
            "1": cobrador.name,
            "2": devedor_nome,
            "3": f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
            "4": divida.description,
        }

        # dispara a task do zap assincronamente

        if divida.phone is not None and divida.phone != "":
            send_whatsapp_task.delay(
                phone=divida.phone,
                variables_dict=variaveis,
            )
            Notification.objects.create(
                user=cobrador,
                charge=divida,
                message=f"WhatsApp enviado para {divida.phone} com variáveis {variaveis}",
                channel="WhatsApp",
                status="Sent",
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

        if divida.email is not None:
            print(f"Enviando email para {divida.email} com assunto '{assunto}'")
            send_email_task.delay(
                to_email=divida.email,
                subject=assunto,
                message=texto_email,
            )
            Notification.objects.create(
                user=cobrador,
                charge=divida,
                message=f"Email enviado para {divida.email} com variáveis {variaveis}",
                channel="Email",
                status="Sent",
            )
