import os

def fix_receipt():
    path = 'banking/templates/banking/receipt.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = [
        (
            '<p class="text-5xl font-extrabold text-gray-900 tracking-tight mb-3">{{ profile.currency }}{{\n                            tx.amount|intcomma }}</p>',
            '<p class="text-5xl font-extrabold text-gray-900 tracking-tight mb-3">{{ profile.currency }}{{ tx.amount|intcomma }}</p>'
        ),
        (
            'Pending <span class="text-green-600 loading-dots mx-1 lowercase"></span> {{\n                            tx.progress_percentage }}%',
            'Pending <span class="text-green-600 loading-dots mx-1 lowercase"></span> {{ tx.progress_percentage }}%'
        ),
        (
            '<p class="text-base font-bold text-gray-900 font-mono mt-0.5">REF-{{\n                                    tx.id|stringformat:"08d" }}-{{ tx.timestamp|date:"ymd" }}</p>',
            '<p class="text-base font-bold text-gray-900 font-mono mt-0.5">REF-{{ tx.id|stringformat:"08d" }}-{{ tx.timestamp|date:"ymd" }}</p>'
        ),
        (
            '<p class="text-base font-bold text-gray-900 mt-0.5">{{ tx.sender.user.first_name }} {{\n                                    tx.sender.user.last_name }}</p>',
            '<p class="text-base font-bold text-gray-900 mt-0.5">{{ tx.sender.user.first_name }} {{ tx.sender.user.last_name }}</p>'
        ),
        (
            '<p class="text-base font-bold text-gray-900 mt-0.5">{{ tx.receiver.user.first_name }} {{\n                                    tx.receiver.user.last_name }}</p>',
            '<p class="text-base font-bold text-gray-900 mt-0.5">{{ tx.receiver.user.first_name }} {{ tx.receiver.user.last_name }}</p>'
        )
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"Replaced in receipt.html")
        else:
            print(f"Could not find replacement in receipt.html:\n{repr(old)}")
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def fix_transfer():
    path = 'banking/templates/banking/transfer.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    replacements = [
        (
            '{{\n                  form.recipient_account.errors.0 }}',
            '{{ form.recipient_account.errors.0 }}'
        ),
        (
            '{{ user.userprofile.currency\n            }}',
            '{{ user.userprofile.currency }}'
        )
    ]
    
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f"Replaced in transfer.html")
        else:
            print(f"Could not find replacement in transfer.html:\n{repr(old)}")
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

fix_receipt()
fix_transfer()
