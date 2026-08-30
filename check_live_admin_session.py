import os
import django

os.environ['DATABASE_URL'] = 'postgresql://apple_bank_user:Qr9WE23xdv9f8fWa2imfNtGma1ZOAWK8@dpg-d9hav8mpbkes73dnac90-a.oregon-postgres.render.com/apple_bank'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client

client = Client()

print("Fetching login page to get CSRF token...")
response = client.get('/secure-admin-portal/login/')
csrf_token = response.cookies.get('csrftoken').value

print("\nLogging in as eluomuno123...")
response = client.post('/secure-admin-portal/login/', {
    'username': 'eluomuno123',
    'password': 'admin123',
    'csrfmiddlewaretoken': csrf_token
})
print("POST status:", response.status_code)
print("Redirect URL:", response.get('Location'))

print("\nNow fetching /secure-admin-portal/ with the same client session...")
response = client.get('/secure-admin-portal/')
print("GET /secure-admin-portal/ status:", response.status_code)
if response.status_code == 302:
    print("Redirected to:", response.get('Location'))
