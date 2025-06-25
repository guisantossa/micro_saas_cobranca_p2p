from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.serializers import CustomTokenCreateSerializer

from .models import UserBankSettings, UserSettings
from .serializers import UserBankSettingsSerializer, UserSettingsSerializer


class CustomAuthTokenView(ObtainAuthToken):
    serializer_class = CustomTokenCreateSerializer

    def post(self, request, *args, **kwargs):
        print("🚀 CustomAuthTokenView disparada!")
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        print(f"✅ Token gerado para user_id={user.id}, cpf={user.cpf}")
        return Response({"auth_token": token.key})


class UserSettingsViewSet(viewsets.ModelViewSet):
    serializer_class = UserSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def user_settings_view(request):
    # Só renderiza o template, sem lógica de get_or_create aqui
    return render(request, "users/user_settings.html")


class UserBankSettingsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserBankSettingsSerializer

    def get_queryset(self):
        return UserBankSettings.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get", "put"], url_path="me")
    def me(self, request):
        try:
            obj = UserBankSettings.objects.get(user=request.user)
        except UserBankSettings.DoesNotExist:
            obj = None

        if request.method == "GET":
            if obj:
                serializer = self.get_serializer(obj)
                return Response(serializer.data)
            return Response({}, status=200)

        if request.method == "PUT":
            if obj:
                serializer = self.get_serializer(obj, data=request.data)
            else:
                serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
