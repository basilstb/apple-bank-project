import re

with open(r'templates\base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add ID to sidebar
content = content.replace(
    '<nav\n        class="hidden md:flex bg-surface-container-low text-primary border-r border-outline-variant fixed left-0 top-0 h-screen w-64 flex-col p-4 space-y-stack-md z-50">',
    '<nav id="sidebar"\n        class="hidden md:flex bg-surface-container-low text-primary border-r border-outline-variant fixed left-0 top-0 h-screen w-64 flex-col p-4 space-y-stack-md z-50 transition-transform duration-300 -translate-x-full md:translate-x-0">'
)

# 2. Add IDs to buttons
content = content.replace(
    '<button class="md:hidden text-on-surface">',
    '<button id="mobile-menu-btn" class="md:hidden text-on-surface p-2 rounded-lg hover:bg-surface-container-high transition-colors">'
)

content = content.replace(
    '<button class="text-on-surface-variant hover:text-primary transition-colors">\n                    <span class="material-symbols-outlined">language</span>\n                </button>',
    '<button id="lang-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">\n                    <span class="material-symbols-outlined">language</span>\n                </button>'
)

content = content.replace(
    '<button class="text-on-surface-variant hover:text-primary transition-colors">\n                    <span class="material-symbols-outlined">notifications</span>\n                </button>',
    '<button id="notif-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">\n                    <span class="material-symbols-outlined">notifications</span>\n                </button>'
)

content = content.replace(
    '<button class="text-on-surface-variant hover:text-primary transition-colors">\n                    <span class="material-symbols-outlined">account_circle</span>\n                </button>',
    '<button id="account-btn" class="text-on-surface-variant hover:text-primary transition-colors p-2 rounded-full hover:bg-surface-container-high">\n                    <span class="material-symbols-outlined">account_circle</span>\n                </button>'
)

# 3. Add script and overlay before </body>
script_block = """
        <!-- Mobile Menu Overlay -->
        <div id="mobile-overlay" class="hidden fixed inset-0 bg-black/50 z-40 md:hidden"></div>

        <script>
            document.addEventListener('DOMContentLoaded', function() {
                const sidebar = document.getElementById('sidebar');
                const mobileMenuBtn = document.getElementById('mobile-menu-btn');
                const overlay = document.getElementById('mobile-overlay');
                
                if (mobileMenuBtn && sidebar && overlay) {
                    // Toggle menu
                    mobileMenuBtn.addEventListener('click', function() {
                        sidebar.classList.toggle('hidden');
                        sidebar.classList.toggle('flex');
                        sidebar.classList.toggle('-translate-x-full');
                        overlay.classList.toggle('hidden');
                    });
                    
                    // Close menu when clicking overlay
                    overlay.addEventListener('click', function() {
                        sidebar.classList.add('hidden');
                        sidebar.classList.remove('flex');
                        sidebar.classList.add('-translate-x-full');
                        overlay.classList.add('hidden');
                    });
                }

                // Top bar buttons interactivity
                const langBtn = document.getElementById('lang-btn');
                const notifBtn = document.getElementById('notif-btn');
                const accountBtn = document.getElementById('account-btn');

                if (langBtn) {
                    langBtn.addEventListener('click', () => alert('Language selection coming soon!'));
                }
                if (notifBtn) {
                    notifBtn.addEventListener('click', () => alert('You have no new notifications.'));
                }
                if (accountBtn) {
                    accountBtn.addEventListener('click', () => alert('Account settings coming soon!'));
                }
            });
        </script>
</body>"""

content = content.replace('</body>', script_block)

with open(r'templates\base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated base.html")
