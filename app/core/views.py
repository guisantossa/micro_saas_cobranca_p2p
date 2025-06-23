from core.models import Charge, Notification
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, permissions

from .serializers import ChargeSerializer, NotificationSerializer


class ChargeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Charge.objects.filter(user=self.request.user)
        name = self.request.query_params.get("name")
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class isOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class ChargeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated, isOwner]

    def get_queryset(self):
        return Charge.objects.filter(user=self.request.user)


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        charge_id = self.request.query_params.get("charge_id")
        user = self.request.user
        qs = Notification.objects.all()

        if charge_id:
            qs = qs.filter(charge__id=charge_id, charge__user=user)
        else:
            qs = qs.none()

        return qs


class PasswordResetConfirmUIDView(View):
    def get(self, request, uid, token, *args, **kwargs):
        return redirect(f"/auth/password/reset/confirm/?uid={uid}&token={token}")


class PasswordResetView(TemplateView):
    template_name = "auth/password_reset.html"


class PasswordResetConfirmView(TemplateView):
    template_name = "auth/password_reset_confirm.html"


# auth
def login(request):
    return render(request, "auth/login.html")


def register(request):
    plan = request.GET.get("plan", "Bronze")  # Default = Bronze
    return render(request, "auth/register.html", {"plan": plan})


def profile(request):
    return render(request, "auth/profile.html")


def edit_profile(request):
    return render(request, "auth/edit_profile.html")


# collections


def charge_details(request, id):
    return render(request, "collections/charge_details.html", {"charge_id": id})


def charges(request):
    return render(request, "collections/charges.html", {"charges": charges})


def dashboard(request):
    return render(request, "collections/dashboard.html")


def new_charges(request):
    if request.method == "POST":
        # Implementar lógica para criar nova cobrança
        pass
    return render(request, "collections/new_charges.html")


def plans(request):
    return render(request, "collections/plans.html")


def reports(request):
    return render(request, "collections/reports.html")


# public


def landing_page(request):
    plans = [
        {
            "name": "Bronze",
            "max_active_charges": 3,
            "allowed_channels": ["mail", "sms"],
            "weekly_charge_limit": 1,
            "priority_support": False,
            "allow_installments": False,
        },
        {
            "name": "Silver",
            "max_active_charges": 5,
            "allowed_channels": ["mail", "sms", "zap"],
            "weekly_charge_limit": 2,
            "priority_support": True,
            "allow_installments": True,
        },
        {
            "name": "Gold",
            "max_active_charges": 10,
            "allowed_channels": ["mail", "sms", "zap"],
            "weekly_charge_limit": 3,
            "priority_support": True,
            "allow_installments": True,
        },
    ]
    return render(request, "public/landing_page.html", {"plans": plans})
