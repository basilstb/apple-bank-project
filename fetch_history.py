import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.models import User

client = Client()
# Log in
logged_in = client.login(username='admin', password='admin123')
print("Login successful:", logged_in)

response = client.get('/history/')
print("Status code:", response.status_code)
html = response.content.decode('utf-8')

# Find the transactions list block
start_idx = html.find('<h2 class="text-xl font-bold text-gray-900">Transaction History</h2>')
if start_idx != -1:
    print(html[start_idx:start_idx+4000])
else:
    print("Could not find Transaction History in HTML")

