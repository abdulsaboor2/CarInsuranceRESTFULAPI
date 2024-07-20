from django.db import models
from django.contrib.auth.models import User
import random
import uuid

class Account(models.Model):
    TYPE_CHOICES = [
        ("regular", "Regular"),
        ("student", "Student"),
        ("saving", "Saving"),
        ("freelance", "Freelance"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_account")
    dob = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.IntegerField()
    postel_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    account_number = models.CharField(max_length=24, unique=True, editable=False)
    status = models.BooleanField(default=False)
    account_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="regular")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super(Account, self).save(*args, **kwargs)

    def generate_account_number(self):
        return ''.join([str(random.randint(0, 9)) for _ in range(24)])

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

TRANSECTION_STATUS = [
    ("deposit", "Deposit"),
    ("withdraw", "Withdraw"),
    ("send", "Send"),
    ("receive", "Receive"),

]

class Transaction(models.Model):
    transaction_id = models.CharField(max_length=25, unique=True, editable=False)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_sent', null=True, blank=True)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions_received')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=TRANSECTION_STATUS, default="send")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super(Transaction, self).save(*args, **kwargs)

    def generate_transaction_id(self):
        return str(uuid.uuid4()).replace("-", "")[:25]

    def __str__(self):
        return f"Transaction {self.transaction_id} from {self.sender.account_number} to {self.receiver.account_number}"
