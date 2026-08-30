import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from banking.models import UserProfile

client = Client()

try:
    user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    if created:
        user.set_password('password123')
        user.save()
    
    profile, p_created = UserProfile.objects.get_or_create(user=user, defaults={'account_number': '1234567890', 'balance': 1000.00})
    
    client.login(username='testuser', password='password123')
    response = client.get('/dashboard/', follow=True)
    print("Dashboard status:", response.status_code)
    print("Dashboard redirect chain:", response.redirect_chain)
    
    if response.status_code == 500:
        print("Dashboard 500 error!")
except Exception as e:
    import traceback
    print("Dashboard exception:")
    traceback.print_exc()
