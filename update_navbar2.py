import os
import re

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Reduce navbar height
# Change py-4 to py-2 in header tags
content = content.replace('py-4 sticky top-0 z-40', 'py-2 sticky top-0 z-40')

# 2. Hide Google Translate widget
content = content.replace('<div class="relative flex items-center">\n                    <div id="google_translate_element"></div>\n                </div>', '<div class="relative flex items-center hidden">\n                    <div id="google_translate_element"></div>\n                </div>')

# 3. Add custom lang dropdown to authenticated header
lang_dropdown_html = """                <div class="relative">
                    <button id="lang-btn" class="text-on-surface-variant hover:text-primary transition-colors p-1 md:p-2 rounded-full hover:bg-surface-container-high">
                        <span class="material-symbols-outlined">language</span>
                    </button>
                    <div id="lang-dropdown" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50 max-h-64 overflow-y-auto">
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="en">English</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="es">Spanish</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="fr">French</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="de">German</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="it">Italian</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="pt">Portuguese</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="zh-CN">Chinese (Simplified)</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="ja">Japanese</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="ko">Korean</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="ar">Arabic</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="ru">Russian</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="hi">Hindi</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="bn">Bengali</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="ur">Urdu</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="id">Indonesian</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="tr">Turkish</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="vi">Vietnamese</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="th">Vietnamese</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="nl">Dutch</a>
                        <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="pl">Dutch</a>
                    </div>
                </div>"""

# Insert into authenticated header
auth_insert_target = """                <div class="relative flex items-center hidden">
                    <div id="google_translate_element"></div>
                </div>"""
if auth_insert_target in content:
    content = content.replace(auth_insert_target, auth_insert_target + '\n' + lang_dropdown_html)

# Insert into unauthenticated header
unauth_insert_target = """                <div class="flex items-center gap-4">
                    <div class="relative flex items-center hidden">
                        <div id="google_translate_element"></div>
                    </div>"""
if unauth_insert_target in content:
    content = content.replace(unauth_insert_target, unauth_insert_target + '\n' + lang_dropdown_html)

# Also reduce the logo text size slightly to help reduce navbar height
content = content.replace('font-headline-lg-mobile md:font-headline-lg text-headline-lg-mobile md:text-headline-lg font-bold text-on-surface', 'text-xl md:text-2xl font-bold text-on-surface')

# Ensure the JS for the custom dropdown is present
js_code = """                // Custom Language Selector Logic
                document.querySelectorAll('.lang-select').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const lang = this.getAttribute('data-lang');
                        const select = document.querySelector('.goog-te-combo');
                        if (select) {
                            select.value = lang;
                            select.dispatchEvent(new Event('change'));
                        }
                        closeAllDropdowns();
                    });
                });"""

if "Custom Language Selector Logic" not in content:
    # Add it before the end of the script tag
    content = content.replace('                if (notifBtn && notifDropdown) {', js_code + '\n                if (notifBtn && notifDropdown) {')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated base.html")
