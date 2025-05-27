from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, cpf, email, password=None, **extra_fields):
        if not cpf:
            raise ValueError("O CPF é obrigatório")
        user = self.model(cpf=cpf, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, cpf, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(cpf, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    cpf = models.CharField(max_length=14, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    telefone = models.CharField(max_length=11, null=True, blank=True)
    nome = models.CharField(max_length=50, null=True, blank=True)
    endereco = models.CharField(max_length=50, null=True, blank=True)
    bairro = models.CharField(max_length=20, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    cidade = models.CharField(max_length=20, null=True, blank=True)
    estado = models.CharField(max_length=20, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    sexo = models.CharField(max_length=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "cpf"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.cpf} - {self.email}"
