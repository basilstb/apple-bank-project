import os

file_path = 'banking/templates/banking/dashboard.html'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = '''      <div class="mt-6 pt-6 border-t border-outline-variant/50 flex gap-4">
        <a href="{% url 'history' %}"
          class="flex-1 text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">View
          Transaction History</a>
        <a href="#"
          class="flex-1 text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">Account
          Details</a>
      </div>'''

replacement = '''      <div class="mt-6 pt-6 border-t border-outline-variant/50 grid grid-cols-2 gap-4">
        <a href="{% url 'history' %}"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">View
          Transaction History</a>
        <a href="#"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">Account
          Details</a>
        <a href="{% url 'loan_application' %}"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">Apply for Loan</a>
        <a href="{% url 'atm_request' %}"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">Apply for ATM Card</a>
      </div>'''

if target in content:
    content = content.replace(target, replacement)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Success")
else:
    print("Target not found")
