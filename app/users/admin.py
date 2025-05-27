from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("id", "cpf", "email", "nome", "telefone", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("cpf", "email", "password")}),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "nome",
                    "telefone",
                    "endereco",
                    "bairro",
                    "cep",
                    "cidade",
                    "estado",
                    "data_nascimento",
                    "sexo",
                )
            },
        ),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas Importantes", {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "cpf",
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )
    search_fields = ("cpf", "email", "nome")
    ordering = ("cpf",)


admin.site.register(CustomUser, CustomUserAdmin)
