import os

file_path = 'templates/base.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_unauth_trans = """                    <div class="relative flex items-center">
                        <div id="google_translate_element"></div>
                    </div>"""

new_unauth_trans = """                    <div class="relative flex items-center" style="position: absolute; left: -9999px;">
                        <div id="google_translate_element"></div>
                    </div>"""

if old_unauth_trans in content:
    content = content.replace(old_unauth_trans, new_unauth_trans)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed unauthenticated translator visibility")
else:
    print("Could not find unauthenticated translator block")
