import phonenumbers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Charge, Notification


class ChargeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    name = serializers.CharField()
    email = serializers.EmailField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    due_date = serializers.DateField(required=False, allow_null=True)
    installment_count = serializers.IntegerField(required=False, allow_null=True)

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

    def validate_email(self, value):
        try:
            validate_email(value)
        except DjangoValidationError:
            raise serializers.ValidationError("Email inválido.")
        return value

    def validate_total_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor deve ser maior que zero.")
        return value

    def validate(self, attrs):
        user = self.context["request"].user
        plan = user.plan

        active_count = Charge.objects.filter(user=user, status="Pending").count()
        print("📊 DEBUG VALIDATE:")
        print(f"Usuário: {user.id} | Plano: {plan}")
        print(
            f"Max Charges Permitidas: {getattr(plan, 'max_active_charges', 'Indefinido')}"
        )
        print(f"Cobranças PENDENTES atuais: {active_count}")
        if plan and active_count >= plan.max_active_charges:
            raise serializers.ValidationError(
                f"Você atingiu o limite de {plan.max_active_charges} cobranças ativas no seu plano."
            )

        return super().validate(attrs)

    def create(self, validated_data):
        user = self.context["request"].user

        # Salva a cobrança local
        charge = Charge.objects.create(
            user=user,
            total_amount=validated_data["total_amount"],
            phone=validated_data["phone"],
            email=validated_data["email"],
            description=validated_data.get("description", ""),
            status="pendente",
        )

        return charge

    class Meta:
        model = Charge
        fields = "__all__"
        read_only_fields = ("user", "asaas_id", "invoice_url")


class ChargeAceiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ["name", "email", "phone", "description", "total_amount"]


class NotificationSerializer(serializers.ModelSerializer):
    charge = serializers.UUIDField(source="charge.id", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "charge", "channel", "sent_at", "status"]
