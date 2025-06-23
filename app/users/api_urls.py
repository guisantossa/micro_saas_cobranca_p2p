from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserSettingsViewSet

router = DefaultRouter()
router.register(r"settings", UserSettingsViewSet, basename="usersettings")

urlpatterns = [
    path("", include(router.urls)),
]
