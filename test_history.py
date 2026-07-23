import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['testserver']

from django.test import Client
from django.contrib.auth.models import User
from banking.models import UserProfile, Transaction

# Create a test user if not exists
user, created = User.objects.get_or_create(username='testuser', defaults={'password': 'password'})
if created:
    user.set_password('password')
    user.save()

profile, _ = UserProfile.objects.get_or_create(user=user)

# Create a dummy transaction
Transaction.objects.get_or_create(
    sender=profile,
    receiver=None,
    amount=100,
    description='Test Deposit',
    transaction_type='Deposit',
    status='Completed'
)

client = Client()
client.login(username='testuser', password='password')

response = client.get('/history/')
print(f"Status code: {response.status_code}")
if response.status_code != 200:
    print(response.content.decode('utf-8'))
else:
    print("History page loaded successfully.")
