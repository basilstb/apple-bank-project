import re

with open('banking/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_receipt = '''    external_receiver_name = None
    external_bank_name = None
    external_account = None
    if not tx.receiver and "Transfer to" in tx.description:
        import re
        # Try new format with account number
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            external_receiver_name = match.group(1)
            external_bank_name = match.group(2)
            external_account = match.group(3)
        else:'''

replacement_receipt = '''    external_receiver_name = None
    external_bank_name = None
    external_account = None
    external_iban = None
    if not tx.receiver and "Transfer to" in tx.description:
        import re
        # Try new format with account number
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            external_receiver_name = match.group(1)
            external_bank_name = match.group(2)
            external_account = match.group(3)
            
            iban_match = re.search(r'\(IBAN: (.*?)\)', tx.description)
            if iban_match:
                external_iban = iban_match.group(1)
        else:'''

if target_receipt in content:
    content = content.replace(target_receipt, replacement_receipt)
    
    target_context = '''    return render(request, 'banking/receipt.html', {
        'tx': tx,
        'external_receiver_name': external_receiver_name,
        'external_bank_name': external_bank_name,
        'external_account': external_account,
        'profile': profile
    })'''
    
    replacement_context = '''    return render(request, 'banking/receipt.html', {
        'tx': tx,
        'external_receiver_name': external_receiver_name,
        'external_bank_name': external_bank_name,
        'external_account': external_account,
        'external_iban': external_iban,
        'profile': profile
    })'''
    
    content = content.replace(target_context, replacement_context)
    
    with open('banking/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Success views.py')
else:
    print('Target not found in views.py')

with open('banking/templates/banking/receipt.html', 'r', encoding='utf-8') as f:
    content = f.read()

target_html = '''                                {% if external_account %}
                                <p class="text-sm font-medium text-gray-600 font-mono">{{ external_account }}</p>
                                {% endif %}'''

replacement_html = '''                                {% if external_account %}
                                <p class="text-sm font-medium text-gray-600 font-mono">{{ external_account }}</p>
                                {% endif %}
                                {% if external_iban %}
                                <p class="text-sm font-medium text-gray-600 font-mono">IBAN: {{ external_iban }}</p>
                                {% endif %}'''

if target_html in content:
    content = content.replace(target_html, replacement_html)
    with open('banking/templates/banking/receipt.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Success receipt.html')
else:
    print('Target not found in receipt.html')
