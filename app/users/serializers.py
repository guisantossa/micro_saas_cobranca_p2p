import phonenumbers
from django.contrib.auth import authenticate
from djoser.serializers import TokenCreateSerializer
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from services.asaas_client import create_or_update_recipient
from validate_docbr import CPF

from .models import User, UserBankSettings, UserSettings


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
                    {"non_field_errors": ["CPF ou senha inválidos."]},
                    code="authorization",
                )
        else:
            raise serializers.ValidationError(
                {"non_field_errors": "Ambos os campos são obrigatórios."},
                code="authorization",
            )

        token, _ = Token.objects.get_or_create(user=user)
        print(f"✅ Token criado ou recuperado para user_id={user.id}, cpf={user.cpf}")

        return {"auth_token": token.key}


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    phone = serializers.CharField(max_length=20)
    re_password = serializers.CharField(write_only=True)

    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = (
            "id",
            "cpf",
            "email",
            "name",
            "phone",
            "password",
            "re_password",
            "address",
            "zipcode",
            "city",
            "state",
            "birth_date",
            "plan",
        )
        extra_kwargs = {"password": {"write_only": True}}

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

    def validate(self, attrs):
        if attrs["password"] != attrs["re_password"]:
            raise serializers.ValidationError(
                {"re_password": "As senhas não coincidem."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password", None)  # remove o campo que não é do modelo
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        # Lista os campos que podem ser editados
        fields = ("id", "cpf", "email", "name", "address", "zipcode", "state", "phone")


PLANOS_LIMITES = {
    "Bronze": 1,
    "Silver": 2,
    "Gold": 3,
}


class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = "__all__"
        read_only_fields = ["user"]

    def validate_cobranca_semanais(self, value):
        maximo = PLANOS_LIMITES.get(self.context["request"].user.plan, 1)
        if value > maximo:
            raise serializers.ValidationError(
                f"Seu plano permite no máximo {maximo} cobranças por semana."
            )
        return value


class UserBankSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBankSettings
        fields = "__all__"
        read_only_fields = ["user", "asaas_recipient_id"]

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        print(instance.__dict__)
        # Linka com Asaas
        recipient = create_or_update_recipient(self.context["request"].user, instance)
        if recipient:
            instance.asaas_recipient_id = recipient["recipient_id"]
            instance.wallet_id = recipient["wallet_id"]
            instance.save()

        return instance

    def create(self, validated_data):
        # Força o usuário autenticado como dono
        user = self.context["request"].user
        validated_data["user"] = user

        instance = super().create(validated_data)

        # Cria no ASAAS
        recipient = create_or_update_recipient(user, instance)
        if recipient:
            instance.asaas_recipient_id = recipient["recipient_id"]
            instance.wallet_id = recipient["wallet_id"]
            instance.save()

        return instance
