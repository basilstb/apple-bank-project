import os

base_path = "templates/base.html"
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the Google Translate widget with the custom dropdown
old_widget = """            <div class="flex items-center gap-4 relative">
                <div class="relative flex items-center">
                    <div id="google_translate_element"></div>
                </div>"""

new_widget = """            <div class="flex items-center gap-4 relative">
                <div class="relative flex items-center hidden">
                    <div id="google_translate_element"></div>
                </div>
                
                <div class="relative">
                    <button id="lang-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">
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
                    </div>
                </div>"""

content = content.replace(old_widget, new_widget)

# 2. Add JavaScript logic
old_js = """                // Top bar buttons interactivity
                const notifBtn = document.getElementById('notif-btn');
                const accountBtn = document.getElementById('account-btn');
                
                const notifDropdown = document.getElementById('notif-dropdown');
                const accountDropdown = document.getElementById('account-dropdown');

                function closeAllDropdowns() {
                    if (notifDropdown) notifDropdown.classList.add('hidden');
                    if (accountDropdown) accountDropdown.classList.add('hidden');
                }"""

new_js = """                // Top bar buttons interactivity
                const langBtn = document.getElementById('lang-btn');
                const notifBtn = document.getElementById('notif-btn');
                const accountBtn = document.getElementById('account-btn');
                
                const langDropdown = document.getElementById('lang-dropdown');
                const notifDropdown = document.getElementById('notif-dropdown');
                const accountDropdown = document.getElementById('account-dropdown');

                function closeAllDropdowns() {
                    if (langDropdown) langDropdown.classList.add('hidden');
                    if (notifDropdown) notifDropdown.classList.add('hidden');
                    if (accountDropdown) accountDropdown.classList.add('hidden');
                }
                
                if (langBtn && langDropdown) {
                    langBtn.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const isHidden = langDropdown.classList.contains('hidden');
                        closeAllDropdowns();
                        if (isHidden) langDropdown.classList.remove('hidden');
                    });
                }

                // Custom Language Selector Logic
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

content = content.replace(old_js, new_js)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched base.html")
