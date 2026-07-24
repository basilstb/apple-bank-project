import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from banking.models import UserProfile

client = Client()
# Create superuser if not exists
su, created = User.objects.get_or_create(username='admin', is_superuser=True, is_staff=True)
if created:
    su.set_password('admin')
    su.save()

client.force_login(su)

# Create a dummy image
image_content = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
profile_pic = SimpleUploadedFile("test_pic.gif", image_content, content_type="image/gif")

# Post to admin user add page
response = client.post('/secure-admin-portal/auth/user/add/', {
    'username': 'testuser2',
    'password': 'testpassword',
    'email': 'test@example.com',
    'first_name': 'Test',
    'last_name': 'User',
    'is_active': 'on',
    'userprofile-TOTAL_FORMS': '1',
    'userprofile-INITIAL_FORMS': '0',
    'userprofile-MIN_NUM_FORMS': '0',
    'userprofile-MAX_NUM_FORMS': '1',
    'userprofile-0-account_number': '1234567890',
    'userprofile-0-balance': '5000.00',
    'userprofile-0-account_status': 'Active',
    'userprofile-0-transaction_pin': '0000',
    'userprofile-0-profile_picture': profile_pic,
})

print(f"Response status: {response.status_code}")
if response.status_code == 200:
    print("Form errors:")
    print(response.context['adminform'].form.errors)
    for inline in response.context['inline_admin_formsets']:
        print(inline.formset.errors)

test_user = User.objects.filter(username='testuser2').first()
if test_user:
    profile = UserProfile.objects.filter(user=test_user).first()
    if profile:
        print(f"Profile picture: {profile.profile_picture}")
    else:
        print("Profile not created.")
else:
    print("User not created.")
