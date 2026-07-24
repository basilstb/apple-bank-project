import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apple_bank.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from banking.models import UserProfile

client = Client()
su = User.objects.get(username='admin')
client.force_login(su)

# Create a dummy image
image_content = b'GIF89a\x01\x00\x01\x00\x80\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;'
profile_pic = SimpleUploadedFile("test_pic2.gif", image_content, content_type="image/gif")

# Post to admin user add page
response = client.post('/secure-admin-portal/auth/user/add/', {
    'username': 'testuser3',
    'password': 'testpassword',
    'email': 'test3@example.com',
    'first_name': 'Test',
    'last_name': 'User',
    'is_active': 'on',
    'userprofile-TOTAL_FORMS': '1',
    'userprofile-INITIAL_FORMS': '0',
    'userprofile-MIN_NUM_FORMS': '0',
    'userprofile-MAX_NUM_FORMS': '1',
    'userprofile-0-account_number': '1234567891',
    'userprofile-0-balance': '5000.00',
    'userprofile-0-account_status': 'Active',
    'userprofile-0-transaction_pin': '0000',
    'userprofile-0-profile_picture': profile_pic,
})

test_user = User.objects.filter(username='testuser3').first()
profile = UserProfile.objects.filter(user=test_user).first()
if profile and profile.profile_picture:
    img_url = profile.profile_picture.url
    print(f"Image URL: {img_url}")
    # Try to fetch the image URL
    res = client.get(img_url)
    print(f"Fetch image status: {res.status_code}")
else:
    print("Profile picture not saved.")
