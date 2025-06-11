from core.models import Charge, Notification
from django.shortcuts import render
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


# auth
def login(request):
    return render(request, "auth/login.html")


def register(request):
    # Implementar autenticação
    return render(request, "auth/register.html")


def profile(request):
    return render(request, "auth/profile.html")


def edit_profile(request):
    return render(request, "auth/edit_profile.html")


def settings(request):
    return render(request, "auth/profile.html")


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
    return render(request, "public/landing_page.html")
