import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.dev")


app = Celery("project")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

from core.notifications.tasks import enviar_lembretes_diarios_task  # noqa: F401 E402
