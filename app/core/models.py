import uuid

from django.db import models
from users.models import User


class Debtor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    cpf = models.CharField(max_length=14, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Charge(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Cancelled", "Cancelled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="charges")
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name="charges")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    due_date = models.DateField()
    installment_count = models.IntegerField()

    def __str__(self):
        return f"{self.debtor.name} - {self.total_amount}"


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
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Sent")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)

    def __str__(self):
        return f"Notification to {self.user.email} via {self.channel}"


class AccessLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="access_logs")
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action}"
