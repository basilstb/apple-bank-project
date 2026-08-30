import re

with open('banking/templates/banking/transfer.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = '                  required id="id_bank_name">\n                {% if form.bank_name.errors %}<p class="text-red-500 text-xs mt-1">{{ form.bank_name.errors.0 }}</p>{% endif %}\n              </div>'
replacement = target + '\n              <div>\n                <label for="id_iban" class="block font-label-md text-label-md text-on-surface-variant mb-1">IBAN (Optional)</label>\n                <input type="text" name="iban"\n                  class="w-full bg-surface border border-slate-200 rounded-lg py-3 px-4 text-on-surface font-body-md focus:outline-none focus:ring-1 focus:ring-primary-container focus:border-primary-container"\n                  id="id_iban">\n                {% if form.iban.errors %}<p class="text-red-500 text-xs mt-1">{{ form.iban.errors.0 }}</p>{% endif %}\n              </div>'

if target in content:
    with open('banking/templates/banking/transfer.html', 'w', encoding='utf-8') as f:
        f.write(content.replace(target, replacement))
    print('Success')
else:
    print('Target not found')
