import phonenumbers
from django.core.exceptions import ValidationError as DjangoValidationError
from django.core.validators import validate_email
from rest_framework import serializers

from .models import Charge, Notification


class ChargeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField()
    email = serializers.EmailField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    whatsapp_authorized = serializers.BooleanField()

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

    def validate_whatsapp_authorized(self, value):
        if not value:
            raise serializers.ValidationError(
                "Você deve confirmar a autorização do devedor para envio via WhatsApp."
            )
        return value

    def can_create_charge(self, user):
        user = self.context["request"].user
        plan = user.plan
        active_count = Charge.objects.filter(user=user, status="Pending").count()
        if active_count >= plan.max_active_charges:
            raise serializers.ValidationError(
                f"Você atingiu o limite de {plan.max_active_charges} cobranças ativas no seu plano."
            )
        return super().validate()

    class Meta:
        model = Charge
        fields = "__all__"
        read_only_fields = ("user",)


class NotificationSerializer(serializers.ModelSerializer):
    charge = serializers.UUIDField(source="charge.id", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "charge", "channel", "sent_at", "status"]
