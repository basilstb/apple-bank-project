import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='eluomuno123')
    u.is_staff = True
    u.is_superuser = True
    u.set_password('admin123')
    u.save()
    print('Success: eluomuno123 is now an admin with password admin123.')
except User.DoesNotExist:
    # If it doesn't exist, create it
    u = User.objects.create_superuser('eluomuno123', 'admin@example.com', 'admin123')
    print('Success: Created new admin user eluomuno123 with password admin123.')
