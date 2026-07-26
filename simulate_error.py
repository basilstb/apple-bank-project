import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.conf import settings
settings.ALLOWED_HOSTS = ['*']

from django.test import Client
from django.contrib.auth.models import User

client = Client()
user = User.objects.first()
if not user:
    user = User.objects.create_user('testuser', 'test@example.com', 'password')

client.force_login(user)

response = client.post('/transfer/', {
    'amount': '100.00',
    'recipient_account': '1234567890',
    'account_name': 'Test User',
    'bank_name': 'Test Bank',
    'swift_code': '',
    'ifsc_code': '',
    'description': 'Test transfer'
})

print(f"Transfer POST status: {response.status_code}")

if response.status_code == 302:
    verify_url = response.url
    print(f"Redirected to: {verify_url}")
    
    # Now simulate POST to verify-pin
    response = client.post(verify_url, {
        'pin': '1234'
    })
    print(f"PIN Verify POST status: {response.status_code}")
    if response.status_code == 500:
        print(response.content.decode())
