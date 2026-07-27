import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User

client = Client(SERVER_NAME='localhost')

# Login
user = User.objects.first()
client.force_login(user)

print("Testing transfer GET...")
response = client.get('/transfer/')
print(f"GET status: {response.status_code}")
if response.status_code == 500:
    print(response.content.decode('utf-8'))

print("Testing transfer POST...")
response = client.post('/transfer/', {
    'amount': '100',
    'recipient_account': '1234567890',
    'account_name': 'Test User',
    'bank_name': 'Nexus Trust Bank',
    'description': 'Test transfer'
})
print(f"POST status: {response.status_code}")
if response.status_code == 500:
    print(response.content.decode('utf-8'))

if response.status_code == 302:
    print("Testing PIN Verify GET...")
    response = client.get('/transfer/verify-pin/')
    print(f"PIN Verify GET status: {response.status_code}")
    if response.status_code == 500:
        print(response.content.decode('utf-8'))
        
    print("Testing PIN Verify POST...")
    response = client.post('/transfer/verify-pin/', {
        'pin': '1234'
    })
    print(f"PIN Verify POST status: {response.status_code}")
    if response.status_code == 500:
        print(response.content.decode('utf-8'))
