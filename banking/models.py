from django.db import models
from django.contrib.auth.models import User
import secrets
import string

def generate_account_number():
    return ''.join(secrets.choice(string.digits) for _ in range(10))

class UserProfile(models.Model):
    ACCOUNT_STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Suspended', 'Suspended'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=10, unique=True, default=generate_account_number)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=5000.00)
    phone_number = models.CharField(max_length=20, blank=True)
    account_status = models.CharField(max_length=20, choices=ACCOUNT_STATUS_CHOICES, default='Active')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    transaction_pin = models.CharField(max_length=128, default='0000')

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('Transfer', 'Transfer'),
        ('Deposit', 'Deposit'),
        ('Withdrawal', 'Withdrawal'),
    )
    STATUS_CHOICES = (
        ('Successful', 'Successful'),
        ('Pending', 'Pending'),
        ('Failed', 'Failed'),
    )
    sender = models.ForeignKey(UserProfile, related_name='sent_transactions', on_delete=models.SET_NULL, null=True, blank=True)
    receiver = models.ForeignKey(UserProfile, related_name='received_transactions', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Successful')
    progress_percentage = models.IntegerField(default=100)

    def save(self, *args, **kwargs):
        if self.progress_percentage >= 100:
            self.progress_percentage = 100
            self.status = 'Successful'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.transaction_type} of ${self.amount} on {self.timestamp.strftime('%Y-%m-%d')}"

class LoanApplication(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='')
    country = models.CharField(max_length=100, default='')
    job = models.CharField(max_length=100, default='')
    email_address = models.EmailField(default='')
    whatsapp_number = models.CharField(max_length=20, default='')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Loan for ${self.amount} by {self.user.user.username} ({self.status})"

class ATMCardRequest(models.Model):
    CARD_TYPE_CHOICES = (
        ('Physical', 'Physical'),
        ('Virtual', 'Virtual'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Issued', 'Issued'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_type} Card Request by {self.user.user.username} ({self.status})"
