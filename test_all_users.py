import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import User
from banking.views import history_view

factory = RequestFactory()

users = User.objects.all()
for user in users:
    try:
        request = factory.get('/history/')
        request.user = user
        response = history_view(request)
        # Render the response to trigger template rendering
        response.render()
        print(f"User {user.username}: Success")
    except Exception as e:
        print(f"User {user.username}: Error - {type(e).__name__}: {str(e)}")
