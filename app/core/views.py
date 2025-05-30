from core.models import Charge, Debtor
from django.shortcuts import redirect, render
from rest_framework import generics, permissions

from .serializers import ChargeSerializer, DebtorSerializer


class ChargeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Charge.objects.filter(user=self.request.user)
        debtor_id = self.request.query_params.get("debtor")
        if debtor_id:
            queryset = queryset.filter(debtor_id=debtor_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ChargeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Charge.objects.all()
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Charge.objects.filter(user=self.request.user)


class DebtorListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = DebtorSerializer
    queryset = Debtor.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class DebtorRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DebtorSerializer
    queryset = Debtor.objects.all()
    permission_classes = [permissions.IsAuthenticated]


# auth
def login(request):
    # Implementar autenticação
    return render(request, "auth/login.html")


def register(request):
    # Implementar autenticação
    return render(request, "auth/register.html")


def profile(request):
    return render(request, "auth/profile.html")


def settings(request):
    return render(request, "auth/profile.html")


# collections


def charge_details(request, id):
    return redirect("charges")
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
    return render(request, "public/landing_page.html")
