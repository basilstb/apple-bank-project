import os

file_path = "templates/base.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Google Translate script to head
head_end = """    </style>
    {% block extra_head %}{% endblock %}
</head>"""

head_replacement = """    </style>
    {% block extra_head %}{% endblock %}
    <style>
        /* Google Translate Customization */
        .goog-te-banner-frame.skiptranslate {
            display: none !important;
        }
        body {
            top: 0px !important;
        }
        #google_translate_element select {
            background-color: #f7f9fb;
            color: #191c1e;
            border: 1px solid #e0e3e5;
            border-radius: 0.5rem;
            padding: 0.5rem;
            font-size: 0.875rem;
            outline: none;
        }
        #google_translate_element select:focus {
            border-color: #ad0012;
            box-shadow: 0 0 0 1px #ad0012;
        }
    </style>
    <script type="text/javascript">
        function googleTranslateElementInit() {
            new google.translate.TranslateElement({pageLanguage: 'en', layout: google.translate.TranslateElement.InlineLayout.SIMPLE}, 'google_translate_element');
        }
    </script>
    <script type="text/javascript" src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
</head>"""

content = content.replace(head_end, head_replacement)

# 2. Replace language dropdown
dropdown_old = """                <div class="relative">
                    <button id="lang-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">
                        <span class="material-symbols-outlined">language</span>
                    </button>
                    <div id="lang-dropdown" class="hidden absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-2 z-50">
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary">English</a>
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary">Spanish</a>
                        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 hover:text-primary">French</a>
                    </div>
                </div>"""

dropdown_new = """                <div class="relative flex items-center">
                    <div id="google_translate_element"></div>
                </div>"""

content = content.replace(dropdown_old, dropdown_new)

# 3. Remove JS logic
js_old = """                const langBtn = document.getElementById('lang-btn');
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

js_new = """                const notifBtn = document.getElementById('notif-btn');
                const accountBtn = document.getElementById('account-btn');
                
                const notifDropdown = document.getElementById('notif-dropdown');
                const accountDropdown = document.getElementById('account-dropdown');

                function closeAllDropdowns() {
                    if (notifDropdown) notifDropdown.classList.add('hidden');
                    if (accountDropdown) accountDropdown.classList.add('hidden');
                }"""

content = content.replace(js_old, js_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched base.html")
