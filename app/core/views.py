from core.models import Charge, Notification
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from services.asaas import create_asaas_charge, get_or_create_asaas_customer

from .serializers import (
    ChargeAceiteSerializer,
    ChargeSerializer,
    NotificationSerializer,
)


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


class ChargeAceiteView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            charge = Charge.objects.get(aceite_token=token, status="pendente")
            serializer = ChargeAceiteSerializer(charge)
            return Response(serializer.data)
        except Charge.DoesNotExist:
            return Response(
                {"error": "Cobrança não encontrada ou já aceita."}, status=404
            )

    def post(self, request, token):
        try:
            charge = Charge.objects.get(aceite_token=token, status="pendente")
        except Charge.DoesNotExist:
            return Response({"error": "Cobrança não encontrada."}, status=404)

        # Cria cliente no ASAAS
        customer_id = get_or_create_asaas_customer(
            {
                "name": request.data.get("name", "no name"),
                "cpfCnpj": request.data.get(
                    "cpfCnpj", "00000000000"
                ),  # CPF é obrigatório
                "email": charge.email,
                "phone": charge.phone,
            }
        )

        # Cria cobrança no ASAAS
        resp = create_asaas_charge(
            customer_id,
            {
                "description": charge.description,
                "total_amount": charge.total_amount,
                "due_date": charge.due_date or timezone.now().date(),
                "billingType": request.data.get("billing_type", "BOLETO"),
            },
            cobrador_recipient_id=charge.user.bank_settings.wallet_id,
        )

        # Atualiza cobrança
        charge.status = "aceita"
        charge.asaas_id = resp.get("id")
        charge.invoice_url = resp.get("invoiceUrl")
        charge.accepted_at = timezone.now()
        charge.save()

        return Response({"status": "ok", "invoice_url": charge.invoice_url})


class AsaasWebhookView(APIView):
    permission_classes = [AllowAny]  # ASAAS não autentica, então libera o acesso

    def post(self, request):
        event_type = request.data.get("event")
        payment = request.data.get("payment")

        if not event_type or not payment:
            return Response(
                {"error": "Dados inválidos"}, status=status.HTTP_400_BAD_REQUEST
            )

        payment_id = payment.get("id")
        payment_status = payment.get("status")

        # DEBUG opcional
        print(
            f"[Webhook ASAAS] Evento: {event_type} | Pagamento ID: {payment_id} | Status: {payment_status}"
        )

        try:
            charge = Charge.objects.get(asaas_id=payment_id)
        except Charge.DoesNotExist:
            return Response({"error": "Cobrança não encontrada"}, status=404)

        # Trate os eventos que interessam
        if event_type == "PAYMENT_RECEIVED":
            charge.status = "paga"
            charge.save()

        elif event_type == "PAYMENT_CONFIRMED":
            charge.status = "paga"
            charge.save()
            pass

        elif event_type == "PAYMENT_DELETED":
            charge.status = "cancelada"
            charge.save()

        return Response({"success": True})


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


def charge_accept(request, token):
    charge = get_object_or_404(Charge, aceite_token=token)
    return render(request, "collections/charge_accept.html", {"charge": charge})


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
