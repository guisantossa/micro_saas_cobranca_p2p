import phonenumbers
from django.contrib.auth import authenticate
from djoser.serializers import TokenCreateSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from validate_docbr import CPF

from .models import User


class CustomTokenCreateSerializer(TokenCreateSerializer):

    cpf = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        cpf = attrs.get("cpf")
        password = attrs.get("password")

        if cpf and password:
            user = authenticate(
                request=self.context.get("request"), username=cpf, password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "CPF ou senha inválidos.", code="authorization"
                )
        else:
            raise serializers.ValidationError(
                "Ambos os campos são obrigatórios.", code="authorization"
            )

        token, _ = Token.objects.get_or_create(user=user)
        print(f"✅ Token criado ou recuperado para user_id={user.id}, cpf={user.cpf}")

        return {"auth_token": token.key}


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    phone = serializers.CharField(max_length=20)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = "__all__"

    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("CPF inválido.")
        return value

    def validate_phone(self, value):
        try:
            parsed_phone = phonenumbers.parse(value, "BR")
            if not phonenumbers.is_valid_number(parsed_phone):
                raise serializers.ValidationError("Número de telefone inválido.")
            return phonenumbers.format_number(
                parsed_phone, phonenumbers.PhoneNumberFormat.E164
            ).replace("+55", "")
        except phonenumbers.NumberParseException:
            raise serializers.ValidationError("Número de telefone mal formatado.")


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        # Lista os campos que podem ser editados
        fields = ("id", "cpf", "email", "name", "address", "zipcode", "state", "phone")
