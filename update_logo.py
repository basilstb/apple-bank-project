import os
import shutil

# Source image path
src_image = r"C:\Users\BASIL\.gemini\antigravity\brain\e11996aa-10ee-4fb1-88e6-82b45b7c3d87\uploaded_image_1785072776916.png"

# Destination directory
dest_dir = r"c:\Users\BASIL\OneDrive\Desktop\APPLE ANTI GRA\banking\static\images"
os.makedirs(dest_dir, exist_ok=True)

# Destination image path
dest_image = os.path.join(dest_dir, "nexus_logo.png")

# Copy the image
shutil.copy2(src_image, dest_image)
print(f"Copied image to {dest_image}")

# Update base.html
file_path = r"c:\Users\BASIL\OneDrive\Desktop\APPLE ANTI GRA\templates\base.html"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace sidebar logo
old_sidebar_logo = '<h1 class="font-headline-lg text-headline-lg text-blue-900 font-bold">Nexus Trust Bank</h1>'
new_sidebar_logo = '<img src="{% static \'images/nexus_logo.png\' %}" alt="Nexus Trust Bank" class="h-10 object-contain">'
content = content.replace(old_sidebar_logo, new_sidebar_logo)

# Replace mobile/unauth header logo
old_header_logo = '<span class="text-xl md:text-2xl font-bold text-on-surface"><span class="text-blue-900 font-bold">Nexus Trust Bank</span></span>'
new_header_logo = '<img src="{% static \'images/nexus_logo.png\' %}" alt="Nexus Trust Bank" class="h-8 md:h-10 object-contain">'
content = content.replace(old_header_logo, new_header_logo)

# Ensure {% load static %} is at the top if not already there
if '{% load static %}' not in content:
    content = content.replace('{% load humanize %}', '{% load humanize %}\n{% load static %}')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated base.html with image logo")
