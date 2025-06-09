from djoser import serializers
from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from validate_docbr import CPF

from .models import User


class CustomUserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        fields = "__all__"

    def validate_cpf(self, value):
        cpf = CPF()
        if not cpf.validate(value):
            raise serializers.ValidationError("CPF inválido.")
        return value


class CustomUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = "__all__"
