import uuid

from django.db import models
from users.models import User


class Charge(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="charges")

    # Dados do Devedor
    name = models.CharField(max_length=50, null=False, blank=False, default="no name")
    phone = models.CharField(max_length=11, null=False, blank=False, default="no phone")
    email = models.EmailField(blank=True, null=True)

    # Dados da Cobrança
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    due_date = models.DateField(blank=True, null=True)
    installment_count = models.IntegerField(blank=True, null=True)
    whatsapp_authorized = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.total_amount}"


class Installment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Overdue", "Overdue"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    charge = models.ForeignKey(
        Charge, on_delete=models.CASCADE, related_name="installments"
    )
    number = models.IntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"Installment {self.number} - {self.status}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ("Pix", "Pix"),
        ("Boleto", "Boleto"),
        ("Transfer", "Transfer"),
        ("Cash", "Cash"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    installment = models.ForeignKey(
        Installment, on_delete=models.CASCADE, related_name="payments"
    )
    payment_date = models.DateField()
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)

    def __str__(self):
        return f"Payment {self.amount_paid} on {self.payment_date}"


class Notification(models.Model):
    STATUS_CHOICES = [
        ("Sent", "Sent"),
        ("Read", "Read"),
    ]

    CHANNEL_CHOICES = [
        ("Email", "Email"),
        ("SMS", "SMS"),
        ("WhatsApp", "WhatsApp"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notifications"
    )
    charge = models.ForeignKey(
        Charge, on_delete=models.CASCADE, related_name="notifications"
    )
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Sent")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)

    def __str__(self):
        return f"Notification to {self.charge_id} via {self.channel}"


class AccessLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="access_logs")
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action}"


class Plan(models.Model):
    PLAN_CHOICES = [
        ("bronze", "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
    ]

    name = models.CharField(max_length=20, choices=PLAN_CHOICES, unique=True)
    max_active_charges = models.PositiveIntegerField()
    allowed_channels = models.JSONField(default=list)  # ['email', 'sms', 'zap']
    weekly_charge_limit = models.PositiveIntegerField()
    priority_support = models.BooleanField(default=False)
    allow_installments = models.BooleanField(default=False)

    def __str__(self):
        return self.get_name_display()
