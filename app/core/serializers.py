from rest_framework import serializers

from .models import Charge, Debtor


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = [
            "id",
            "user",
            "debtor",
            "total_amount",
            "created_at",
            "description",
            "status",
            "due_date",
            "installment_count",
        ]
        read_only_fields = ["id", "user", "created_at", "status"]


class DebtorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debtor
        fields = ["id", "name", "phone", "email", "cpf", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
