import os

file_path = 'apple_bank/settings.py'
with open(file_path, 'r') as f:
    content = f.read()

# Add to INSTALLED_APPS
apps_str = "'django.contrib.staticfiles',"
new_apps_str = apps_str + "\n    'cloudinary_storage',\n    'cloudinary',"
content = content.replace(apps_str, new_apps_str)

# Add DEFAULT_FILE_STORAGE
content += "\n# Cloudinary Media Storage\nDEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'\n"

with open(file_path, 'w') as f:
    f.write(content)
