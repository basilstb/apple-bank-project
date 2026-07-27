import os

file_path = r"c:\Users\BASIL\OneDrive\Desktop\APPLE ANTI GRA\banking\templates\banking\dashboard.html"

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_block = """        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-1">Total
              Available Balance</h2>"""

new_block = """        <div class="flex justify-between items-center mb-8 pb-6 border-b border-outline-variant/30">
          <div class="flex items-center gap-4">
            {% if user.userprofile.profile_picture %}
            <img class="w-16 h-16 rounded-full object-cover shadow-md border-2 border-primary/20"
                src="{{ user.userprofile.profile_picture.url }}" alt="Profile Picture" />
            {% else %}
            <div
                class="w-16 h-16 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-bold text-xl shadow-md border-2 border-primary/20">
                {{ user.first_name|first }}{{ user.last_name|first }}
            </div>
            {% endif %}
            <div>
              <h2 class="font-headline-lg text-2xl md:text-3xl font-bold text-on-surface">Welcome, {{ user.first_name }}!</h2>
              <p class="font-body-sm text-body-sm text-on-surface-variant">Here's your account overview</p>
            </div>
          </div>
        </div>

        <div class="flex justify-between items-start mb-6">
          <div>
            <h2 class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-1">Total
              Available Balance</h2>"""

content = content.replace(old_block, new_block)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
