import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.template.loader import get_template

try:
    get_template('base.html')
    print("base.html loaded successfully without syntax errors.")
except Exception as e:
    print(f"Error loading base.html: {e}")
