import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.hashers import check_password

try:
    print(check_password("1234", ""))
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
