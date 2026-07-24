import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
if user:
    client.force_login(user)
    try:
        response = client.get('/history/')
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print(response.content.decode())
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("No users found.")
