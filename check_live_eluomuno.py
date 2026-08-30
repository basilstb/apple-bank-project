import os
import django

os.environ['DATABASE_URL'] = 'postgresql://apple_bank_user:Qr9WE23xdv9f8fWa2imfNtGma1ZOAWK8@dpg-d9hav8mpbkes73dnac90-a.oregon-postgres.render.com/apple_bank'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

print("Authenticating eluomuno...")
user = authenticate(username='eluomuno', password='admin123')
print("Result:", user)
if user:
    print(f"is_active: {user.is_active}, is_staff: {user.is_staff}, is_superuser: {user.is_superuser}")
