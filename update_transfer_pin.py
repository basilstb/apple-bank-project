import os

file_path = r"c:\Users\BASIL\OneDrive\Desktop\APPLE ANTI GRA\banking\templates\banking\transfer_pin.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """                    <div class="flex justify-between">
                        <span class="text-on-surface-variant text-sm">Amount:</span>
                        <span class="font-bold text-on-surface">{{ user.userprofile.currency }}{{
                            transfer_data.amount|intcomma }}</span>
                    </div>"""

new_block = """                    <div class="flex justify-between">
                        <span class="text-on-surface-variant text-sm">Amount:</span>
                        <span class="font-bold text-on-surface">{{ user.userprofile.currency }}{{ transfer_data.amount|intcomma }}</span>
                    </div>"""

content = content.replace(old_block, new_block)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
