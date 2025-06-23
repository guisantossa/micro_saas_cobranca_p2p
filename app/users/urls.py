from django.urls import path

from .views import user_settings_view

urlpatterns = [
    path("settings/", user_settings_view, name="user_settings"),
]
