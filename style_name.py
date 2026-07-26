import os

def replace_in_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    new_content = content
    for old, new in replacements:
        new_content = new_content.replace(old, new)
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")

# base.html
replace_in_file('templates/base.html', [
    ('<h1 class="font-headline-lg text-headline-lg text-primary">Nexus Trust Bank</h1>', '<h1 class="font-headline-lg text-headline-lg text-blue-900 font-bold">Nexus Trust Bank</h1>'),
    ('                    Nexus Trust Bank', '                    <span class="text-blue-900 font-bold">Nexus Trust Bank</span>'),
    ('© 2026 Nexus Trust Bank.', '© 2026 <span class="text-blue-900 font-bold">Nexus Trust Bank</span>.')
])

# register.html
replace_in_file('banking/templates/banking/register.html', [
    ('Join Nexus Trust Bank and get', 'Join <span class="text-blue-900 font-bold">Nexus Trust Bank</span> and get')
])

# receipt.html
replace_in_file('banking/templates/banking/receipt.html', [
    ('<h2 class="text-2xl font-bold text-gray-900 tracking-tight">Nexus Trust Bank</h2>', '<h2 class="text-2xl font-bold text-blue-900 tracking-tight">Nexus Trust Bank</h2>'),
    ('<p class="text-xs font-medium text-gray-500">Nexus Trust Bank</p>', '<p class="text-xs font-medium text-blue-900 font-bold">Nexus Trust Bank</p>')
])

# dashboard.html
replace_in_file('banking/templates/banking/dashboard.html', [
    ('        Nexus Trust Bank.</p>', '        <span class="text-blue-900 font-bold">Nexus Trust Bank</span>.</p>')
])

# atm_request.html
replace_in_file('banking/templates/banking/atm_request.html', [
    ('<span class="font-headline-lg text-[10px] text-on-surface opacity-70">Nexus Trust Bank</span>', '<span class="font-headline-lg text-[10px] text-blue-900 font-bold opacity-70">Nexus Trust Bank</span>'),
    ('<span class="font-headline-lg text-[10px] text-on-primary opacity-90">Nexus Trust Bank</span>', '<span class="font-headline-lg text-[10px] text-blue-900 font-bold opacity-90">Nexus Trust Bank</span>')
])

print("Styling complete.")
