import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.models import User

try:
    u = User.objects.get(username='basilstb')
    u.is_staff = True
    u.is_superuser = True
    u.save()
    print('Success: basilstb is now an admin.')
except User.DoesNotExist:
    print('Error: User basilstb does not exist.')
