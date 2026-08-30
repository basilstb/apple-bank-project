import re

with open('banking/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

target_download = '''    if tx.receiver:
        details.append(("Receiver Name", f"{tx.receiver.user.first_name} {tx.receiver.user.last_name}"))
        details.append(("Receiver Account", tx.receiver.account_number))
    elif "Transfer to" in tx.description:
        import re
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            details.append(("Receiver Name", match.group(1)))
            details.append(("Receiver Account", match.group(3)))
            details.append(("Bank Name", match.group(2)))
        else:'''

replacement_download = '''    if tx.receiver:
        details.append(("Receiver Name", f"{tx.receiver.user.first_name} {tx.receiver.user.last_name}"))
        details.append(("Receiver Account", tx.receiver.account_number))
    elif "Transfer to" in tx.description:
        import re
        match = re.search(r'Transfer to (.*?) at (.*?) \(Acct: (.*?)\)', tx.description)
        if match:
            details.append(("Receiver Name", match.group(1)))
            details.append(("Receiver Account", match.group(3)))
            details.append(("Bank Name", match.group(2)))
            
            iban_match = re.search(r'\(IBAN: (.*?)\)', tx.description)
            if iban_match:
                details.append(("IBAN", iban_match.group(1)))
        else:'''

if target_download in content:
    content = content.replace(target_download, replacement_download)
    with open('banking/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Success download_receipt_view')
else:
    print('Target not found in download_receipt_view')
