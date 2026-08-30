import os
import django

os.environ['DATABASE_URL'] = 'postgresql://apple_bank_user:Qr9WE23xdv9f8fWa2imfNtGma1ZOAWK8@dpg-d9hav8mpbkes73dnac90-a.oregon-postgres.render.com/apple_bank'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

print("Testing authenticate() on live database:")
user1 = authenticate(username='admin', password='Admin123!')
print("admin auth result:", user1)

user2 = authenticate(username='eluomuno123', password='admin123')
print("eluomuno123 auth result:", user2)

# Check if they are active
if user1:
    print(f"admin is_active: {user1.is_active}, is_staff: {user1.is_staff}, is_superuser: {user1.is_superuser}")
if user2:
    print(f"eluomuno123 is_active: {user2.is_active}, is_staff: {user2.is_staff}, is_superuser: {user2.is_superuser}")
