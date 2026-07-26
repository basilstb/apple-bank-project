import os

file_path = 'banking/templates/banking/dashboard.html'
with open(file_path, 'r') as f:
    content = f.read()

target = """      <div class="mt-6 pt-6 border-t border-outline-variant/50 grid grid-cols-2 gap-4">
        <a href="{% url 'history' %}"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">View
          Transaction History</a>"""

replacement = """      <div class="mt-6 pt-6 border-t border-outline-variant/50 grid grid-cols-2 gap-4">
        <a href="{% url 'transfer' %}"
          class="text-center bg-green-600 text-white py-2 rounded-lg font-label-md text-label-md hover:bg-green-700 transition-colors shadow-sm col-span-2">Transfer</a>
        <a href="{% url 'history' %}"
          class="text-center bg-surface-container text-on-surface py-2 rounded-lg font-label-md text-label-md hover:bg-surface-container-highest transition-colors border border-outline-variant">View
          Transaction History</a>"""

new_content = content.replace(target, replacement)

with open(file_path, 'w') as f:
    f.write(new_content)

print("Patched dashboard.html")
