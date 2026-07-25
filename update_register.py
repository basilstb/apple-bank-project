import os

file_path = 'banking/templates/banking/register.html'
with open(file_path, 'r') as f:
    content = f.read()

old_text = """        <div class="text-center mt-4">
            <a href="{% url 'login' %}" class="font-medium text-apple-dark hover:text-gray-700 text-sm">
                Already have an account? Sign in
            </a>
        </div>"""

new_text = """        <div class="text-center mt-6 flex flex-col items-center space-y-3">
            <span class="text-sm text-gray-600">Already have an account?</span>
            <a href="{% url 'login' %}" style="background-color: #10b981; color: white;" class="inline-flex justify-center py-2 px-6 border border-transparent text-sm font-medium rounded-full hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-colors shadow-sm">
                Sign in
            </a>
        </div>"""

if old_text in content:
    content = content.replace(old_text, new_text)
else:
    print("Old text not found in register.html!")

with open(file_path, 'w') as f:
    f.write(content)
