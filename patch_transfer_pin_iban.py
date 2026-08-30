import re

with open('banking/templates/banking/transfer_pin.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '                    <div class="flex justify-between">\n                        <span class="text-on-surface-variant text-sm">Account Number:</span>\n                        <span class="font-bold text-on-surface">{{ transfer_data.recipient_account }}</span>\n                    </div>'
replacement = target + '\n                    {% if transfer_data.iban %}\n                    <div class="flex justify-between">\n                        <span class="text-on-surface-variant text-sm">IBAN:</span>\n                        <span class="font-bold text-on-surface">{{ transfer_data.iban }}</span>\n                    </div>\n                    {% endif %}'

if target in content:
    with open('banking/templates/banking/transfer_pin.html', 'w', encoding='utf-8') as f:
        f.write(content.replace(target, replacement))
    print('Success')
else:
    print('Target not found')
