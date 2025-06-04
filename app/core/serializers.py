from rest_framework import serializers

from .models import Charge, Notification


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = "__all__"
        read_only_fields = ("user",)


class NotificationSerializer(serializers.ModelSerializer):
    charge = serializers.UUIDField(source="charge.id", read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "charge", "type", "sent_at", "status"]
