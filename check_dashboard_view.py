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

response = client.get('/dashboard/')
print("Dashboard status:", response.status_code)
if response.status_code == 500:
    print("Dashboard 500 error!")
