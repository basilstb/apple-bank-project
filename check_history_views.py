import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from banking.models import UserProfile, Transaction

client = Client()

user = User.objects.get(username='admin')
client.force_login(user)

response = client.get('/history/')
print("History status:", response.status_code)
if response.status_code == 500:
    print("History 500 error!")

tx = Transaction.objects.first()
if tx:
    response = client.get(f'/receipt/{tx.id}/')
    print("Receipt status:", response.status_code)
    if response.status_code == 500:
        print("Receipt 500 error!")
