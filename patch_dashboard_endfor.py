import re

def fix_dashboard():
    with open('banking/templates/banking/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the broken block
    pattern = r'<div class="mt-4 pl-2">\s*<div class="flex justify-between text-xs font-label-md text-on-surface-variant mb-1">\s*<span>Amount</span>\s*<span>{{ user\.userprofile\.currency }}{{ loan\.amount\|intcomma }}</span>\s*</div>\s*</div>\s*</div>'
    
    replacement = '''<div class="mt-4 pl-2">
            <div class="flex justify-between text-xs font-label-md text-on-surface-variant mb-1">
              <span>Amount</span>
              <span>{{ user.userprofile.currency }}{{ loan.amount|intcomma }}</span>
            </div>
            <div class="w-full bg-surface-container-highest rounded-full h-1.5">
              <div class="bg-primary-container h-1.5 rounded-full"
                style="width:{% if loan.status == 'Approved' %}100{% elif loan.status == 'Pending' %}50{% else %}30{% endif %}%">
              </div>
            </div>
            <p class="text-xs text-on-surface-variant mt-2 font-body-sm">{% if loan.status == 'Pending' %}Awaiting verification.{% elif loan.status == 'Approved' %}Application approved.{% else %}Application rejected.{% endif %}</p>
          </div>
        </div>
        {% empty %}
        <div class="text-center py-4 text-on-surface-variant font-body-sm">No loan applications found.</div>
        {% endfor %}
      </div>
    </div>
  </div>'''
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open('banking/templates/banking/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

fix_dashboard()
print('Dashboard fixed')
