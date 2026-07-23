import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from banking.models import Transaction

admin = User.objects.filter(is_superuser=True).first()
if admin:
    client = Client()
    client.force_login(admin)
    
    # Try to access the admin history page for a transaction
    tx = Transaction.objects.first()
    if tx:
        response = client.get(f'/admin/banking/transaction/{tx.id}/history/')
        print(f"Transaction admin history status: {response.status_code}")
        if response.status_code != 200:
            print(response.content.decode('utf-8')[:500])
    
    # Try to access the admin history page for a user profile
    from banking.models import UserProfile
    profile = UserProfile.objects.first()
    if profile:
        response = client.get(f'/admin/banking/userprofile/{profile.id}/history/')
        print(f"UserProfile admin history status: {response.status_code}")
        if response.status_code != 200:
            print(response.content.decode('utf-8')[:500])
