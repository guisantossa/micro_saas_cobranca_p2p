from core.models import Charge


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
            "1": getattr(cobrador, "name", "")
            or getattr(cobrador, "username", "")
            or " ",
            "2": devedor_nome,
            "3": f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
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
