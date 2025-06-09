import os

from django.core.mail import send_mail

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")


send_mail(
    "Teste SendGrid",
    "Se tu receber isso, SendGrid tá funcionando!",
    "seuemail@sendgrid.net",
    ["gui.santos.sa@gmail.com"],
    fail_silently=False,
)
