"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from core import views
from core.views import (
    AsaasWebhookView,
    ChargeAceiteView,
    ChargeListCreateAPIView,
    ChargeRetrieveUpdateDestroyAPIView,
    NotificationListView,
    PasswordResetConfirmUIDView,
    PasswordResetConfirmView,
    PasswordResetView,
)
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from users.views import CustomAuthTokenView

urlpatterns = [
    path("admin/", admin.site.urls),
]


@require_GET
@csrf_exempt
def health_check(request):
    print("Health check hit")
    return JsonResponse({"status": "ok"}, status=200)


# app/project/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    # public
    path("", views.landing_page, name="index"),
    # auth_users
    path("auth/", include("djoser.urls")),  # Djoser endpoints
    path("auth/", include("djoser.urls.authtoken")),  # Token endpoints
    path("auth/token/login/", CustomAuthTokenView.as_view(), name="custom_login"),
    path("auth/password/reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "auth/password/reset/confirm/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "auth/password/reset/confirm/<uid>/<token>/",
        PasswordResetConfirmUIDView.as_view(),
        name="password_reset_confirm_uid",
    ),
    path("health/", health_check),
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit-profile"),
    path("register/", views.register, name="register"),
    # collections
    path("dashboard/", views.dashboard, name="dashboard"),
    path("charges/", views.charges, name="charges"),
    path("charge_details/<uuid:id>/", views.charge_details, name="charge-details"),
    path("new_charges/", views.new_charges, name="new-charges"),
    path("plans/", views.new_charges, name="plans"),
    path("reports/", views.reports, name="reports"),
    # apis
    path("api/charges/", ChargeListCreateAPIView.as_view(), name="charge-list-create"),
    path(
        "api/charges/<uuid:pk>/",
        ChargeRetrieveUpdateDestroyAPIView.as_view(),
        name="charge-list-details",
    ),
    path(
        "api/notifications/",
        NotificationListView.as_view(),
        name="notification-list-api",
    ),
    path("users/", include("users.urls")),
    path("api/users/", include("users.api_urls")),
    path("user_settings/", lambda request: redirect("user_settings")),
    path(
        "api/charges/accept/<uuid:token>/",
        ChargeAceiteView.as_view(),
        name="charge-aceite",
    ),
    path("aceite/<uuid:token>/", views.charge_accept, name="charge-aceite"),
    path("asaas/webhook/", AsaasWebhookView.as_view(), name="asaas-webhook"),
]
