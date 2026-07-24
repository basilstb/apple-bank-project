import os
import django

os.environ['DATABASE_URL'] = 'postgresql://apple_bank_user:Qr9WE23xdv9f8fWa2imfNtGma1ZOAWK8@dpg-d9hav8mpbkes73dnac90-a.oregon-postgres.render.com/apple_bank'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'Admin123!')
    print('Superuser created successfully on live database.')
else:
    user = User.objects.get(username='admin')
    user.set_password('Admin123!')
    user.save()
    print('Password reset for existing admin on live database.')
