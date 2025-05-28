from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("id", "cpf", "email", "name", "phone", "is_active", "is_staff")
    list_filter = ("is_active", "is_staff")
    fieldsets = (
        (None, {"fields": ("cpf", "email", "password")}),
        (
            "Informações Pessoais",
            {
                "fields": (
                    "nome",
                    "phone",
                    "adress",
                    "city",
                    "zipcode",
                    "state",
                    "estado",
                    "birth_date",
                    "gender",
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


admin.site.register(User, CustomUserAdmin)
