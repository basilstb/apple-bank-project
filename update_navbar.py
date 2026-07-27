import os
import re

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Change header background
content = content.replace('bg-surface-container-lowest', 'bg-blue-50')

# 2. Unhide translator in authenticated header
old_auth_trans = """                <div class="relative flex items-center hidden">
                    <div id="google_translate_element"></div>
                </div>"""
new_auth_trans = """                <div class="relative flex items-center">
                    <div id="google_translate_element"></div>
                </div>"""
content = content.replace(old_auth_trans, new_auth_trans)

# 3. Remove custom lang dropdown
lang_dropdown_regex = r'<div class="relative">\s*<button id="lang-btn".*?</button>\s*<div id="lang-dropdown".*?</div>\s*</div>'
content = re.sub(lang_dropdown_regex, '', content, flags=re.DOTALL)

# 4. Update unauthenticated header right side
old_unauth_right = """                <div class="flex items-center gap-4">
                    <a href="{% url 'login' %}"
                        class="text-on-surface-variant hover:text-primary transition-colors">Login</a>
                    <a href="{% url 'register' %}"
                        class="bg-primary-container text-on-primary px-4 py-2 rounded-lg font-label-md text-label-md hover:bg-primary transition-colors shadow-sm">Open
                        Account</a>
                </div>"""
new_unauth_right = """                <div class="flex items-center gap-4">
                    <div class="relative flex items-center">
                        <div id="google_translate_element"></div>
                    </div>
                    <a href="{% url 'login' %}"
                        class="text-on-surface-variant hover:text-primary transition-colors font-bold">Login</a>
                </div>"""
content = content.replace(old_unauth_right, new_unauth_right)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated base.html")
