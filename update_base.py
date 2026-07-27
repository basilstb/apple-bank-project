import os

file_path = r"c:\Users\BASIL\OneDrive\Desktop\APPLE ANTI GRA\templates\base.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace unauthenticated header translator
old_unauth = """                <div class="flex items-center gap-4">
                    <div class="relative flex items-center" style="position: absolute; left: -9999px;">
                        <div id="google_translate_element"></div>
                    </div>
                    <a href="{% url 'login' %}"
                        class="text-on-surface-variant hover:text-primary transition-colors font-bold">Login</a>
                </div>"""

new_unauth = """                <div class="flex items-center gap-4">
                    <div class="relative flex items-center" style="position: absolute; left: -9999px;">
                        <div id="google_translate_element"></div>
                    </div>
                    
                    <div class="relative">
                        <button id="lang-btn-unauth" class="text-on-surface-variant hover:text-primary transition-colors p-1 md:p-2 rounded-full hover:bg-surface-container-high">
                            <span class="material-symbols-outlined" translate="no">language</span>
                        </button>
                        <div id="lang-dropdown-unauth" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50 max-h-64 overflow-y-auto">
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
                            <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="th">Thai</a>
                            <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="nl">Dutch</a>
                            <a href="#" class="lang-select block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary" data-lang="pl">Polish</a>
                        </div>
                    </div>

                    <a href="{% url 'login' %}"
                        class="text-on-surface-variant hover:text-primary transition-colors font-bold">Login</a>
                </div>"""

content = content.replace(old_unauth, new_unauth)

# 2. Update JS
old_js = """                const langBtn = document.getElementById('lang-btn');
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
                }"""

new_js = """                const langBtn = document.getElementById('lang-btn');
                const langBtnUnauth = document.getElementById('lang-btn-unauth');
                const notifBtn = document.getElementById('notif-btn');
                const accountBtn = document.getElementById('account-btn');
                
                const langDropdown = document.getElementById('lang-dropdown');
                const langDropdownUnauth = document.getElementById('lang-dropdown-unauth');
                const notifDropdown = document.getElementById('notif-dropdown');
                const accountDropdown = document.getElementById('account-dropdown');

                function closeAllDropdowns() {
                    if (langDropdown) langDropdown.classList.add('hidden');
                    if (langDropdownUnauth) langDropdownUnauth.classList.add('hidden');
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

                if (langBtnUnauth && langDropdownUnauth) {
                    langBtnUnauth.addEventListener('click', (e) => {
                        e.stopPropagation();
                        const isHidden = langDropdownUnauth.classList.contains('hidden');
                        closeAllDropdowns();
                        if (isHidden) langDropdownUnauth.classList.remove('hidden');
                    });
                }"""

content = content.replace(old_js, new_js)

# 3. Update profile picture
old_profile = """                <div class="relative">
                    <button id="account-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">
                        <span class="material-symbols-outlined" translate="no">account_circle</span>
                    </button>"""

new_profile = """                <div class="relative">
                    <button id="account-btn" class="text-on-surface-variant hover:text-primary transition-colors p-1 md:p-2 rounded-full hover:bg-surface-container-high flex items-center justify-center">
                        {% if user.userprofile.profile_picture %}
                        <img class="w-8 h-8 rounded-full object-cover shadow-sm" src="{{ user.userprofile.profile_picture.url }}" alt="Profile" />
                        {% else %}
                        <span class="material-symbols-outlined" translate="no">account_circle</span>
                        {% endif %}
                    </button>"""

content = content.replace(old_profile, new_profile)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
