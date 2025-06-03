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
from core.views import ChargeListCreateAPIView, ChargeRetrieveUpdateDestroyAPIView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
]


# app/project/urls.py
urlpatterns = [
    path("admin/", admin.site.urls),
    # public
    path("", views.landing_page, name="index"),
    # auth_users
    path("auth/", include("djoser.urls")),  # Djoser endpoints
    path("auth/", include("djoser.urls.authtoken")),  # Token endpoints
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit-profile"),
    path("register/", views.register, name="register"),
    path("settings/", views.settings, name="settings"),
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
]
