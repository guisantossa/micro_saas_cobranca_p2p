import uuid

from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.postgres.fields import ArrayField
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("CPF is required")
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(cpf, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    address_number = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=8, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=2, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    plan = models.ForeignKey(
        "core.Plan", on_delete=models.SET_NULL, null=True, blank=True
    )

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserSettings(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings"
    )
    cobranca_semanais = models.PositiveIntegerField(default=0)
    dias_disparo = ArrayField(models.CharField(max_length=10), default=list, blank=True)
    horario_envio = models.TimeField(null=True, blank=True)
    notificar_pago = models.BooleanField(default=True)
    notificar_falha_envio = models.BooleanField(default=True)

    def __str__(self):
        return f"Configurações de {self.user}"


class UserBankSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    asaas_recipient_id = models.CharField(max_length=100, blank=True, null=True)
    bank_code = models.CharField(max_length=10)
    agency = models.CharField(max_length=10)
    account = models.CharField(max_length=20)
    account_digit = models.CharField(max_length=5)
    account_type = models.CharField(
        max_length=10,
        choices=[
            ("CHECKING", "Conta Corrente"),
            ("SAVINGS", "Conta Poupança"),
        ],
    )

    def __str__(self):
        return f"Dados bancários de {self.user}"
