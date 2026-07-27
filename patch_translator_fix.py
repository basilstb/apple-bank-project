import os
import re

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove 'hidden' from the Google Translate container
content = content.replace('<div class="relative flex items-center hidden">\n                    <div id="google_translate_element"></div>\n                </div>', '<div class="relative flex items-center" style="position: absolute; left: -9999px;">\n                    <div id="google_translate_element"></div>\n                </div>')

# 2. Fix duplicated labels in the dropdown
content = content.replace('data-lang="th">Vietnamese</a>', 'data-lang="th">Thai</a>')
content = content.replace('data-lang="pl">Dutch</a>', 'data-lang="pl">Polish</a>')

# 3. Update the JS to trigger the change event more reliably
old_js = """                        const select = document.querySelector('.goog-te-combo');
                        if (select) {
                            select.value = lang;
                            select.dispatchEvent(new Event('change'));
                        }"""

new_js = """                        const select = document.querySelector('.goog-te-combo');
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
                        }"""

content = content.replace(old_js, new_js)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed translator in base.html")
