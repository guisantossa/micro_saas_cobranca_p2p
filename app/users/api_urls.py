from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserBankSettingsViewSet, UserSettingsViewSet

router = DefaultRouter()
router.register(r"settings", UserSettingsViewSet, basename="usersettings")
router.register(r"bank", UserBankSettingsViewSet, basename="userbanksettings")

urlpatterns = [
    path("", include(router.urls)),
]
