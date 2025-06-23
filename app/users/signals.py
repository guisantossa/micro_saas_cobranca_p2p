from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserSettings


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_settings_padrao(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)
        print(f"✅ Configurações padrão criadas para o usuário {instance.cpf}")
