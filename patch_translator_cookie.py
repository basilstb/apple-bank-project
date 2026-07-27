import os

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_js = """                // Custom Language Selector Logic
                document.querySelectorAll('.lang-select').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const lang = this.getAttribute('data-lang');
                        const select = document.querySelector('.goog-te-combo');
                        if (select) {
                            select.value = lang;
                            // Trigger change event in a way that Google Translate recognizes
                            if (typeof Event === 'function') {
                                select.dispatchEvent(new Event('change', { bubbles: true }));
                            } else {
                                const event = document.createEvent('HTMLEvents');
                                event.initEvent('change', true, true);
                                select.dispatchEvent(event);
                            }
                        }
                        closeAllDropdowns();
                    });
                });"""

new_js = """                // Custom Language Selector Logic (Cookie Method)
                document.querySelectorAll('.lang-select').forEach(item => {
                    item.addEventListener('click', function(e) {
                        e.preventDefault();
                        const lang = this.getAttribute('data-lang');
                        
                        if (lang === 'en') {
                            document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                            document.cookie = `googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname};`;
                        } else {
                            document.cookie = `googtrans=/en/${lang}; path=/`;
                            document.cookie = `googtrans=/en/${lang}; path=/; domain=${window.location.hostname}`;
                        }
                        
                        window.location.reload();
                    });
                });"""

if old_js in content:
    content = content.replace(old_js, new_js)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Updated base.html with cookie method")
else:
    print("Could not find old JS block")
