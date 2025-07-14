from datetime import timedelta

from core.models import Charge, Notification
from django.utils import timezone


def enviar_lembretes_diarios():
    from .tasks import send_email_task, send_whatsapp_task

    hoje = timezone.now()
    uma_semana_atras = hoje - timedelta(days=7)

    # pega as cobranças vencendo hoje e que ainda não foram pagas
    dividas = Charge.objects.exclude(status__in=["pago", "cancelada"])
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
        descricao = divida.description or "Cobrança pendente"

        if divida.invoice_url is not None and divida.invoice_url != "":
            url_cobranca = divida.invoice_url
        else:
            url_cobranca = f"https://www.cobraii.com.br/aceite/{divida.aceite_token}/"

        # prepara mensagem pro zap (as variáveis que o template espera)
        variaveis = {
            "autor": cobrador.name,
            "valor": f"{valor:,.2f}".replace(",", "X")
            .replace(".", ",")
            .replace("X", "."),
            "nome": devedor_nome,
            "descricao": descricao,
            "url": url_cobranca,
        }

        # dispara a task do zap assincronamente

        if divida.phone is not None and divida.phone != "":
            print(f"Enviando WhatsApp para {divida.phone} com variáveis {variaveis}")
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
        Sr.(a) {variaveis['nome']},

        Lembramos que tem uma dívida em aberto com o Sr.(a) {variaveis['autor']}, no valor de
        R$ {variaveis['valor']}. Referente à dívida: {variaveis['descricao']}.
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
