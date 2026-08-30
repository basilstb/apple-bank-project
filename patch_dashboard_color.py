import re

def fix_dashboard():
    with open('banking/templates/banking/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the button color
    content = content.replace('bg-[#25D366]', 'bg-blue-600')
    content = content.replace('hover:bg-[#20ba5a]', 'hover:bg-blue-700')

    with open('banking/templates/banking/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_dashboard()
print('Dashboard fixed')
