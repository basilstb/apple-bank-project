import sys
import re

with open('banking/templates/banking/receipt.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<span class=\"inline-flex items-center px-4 py-1\.5 rounded-full text-sm font-bold uppercase tracking-wider print-exact\s*{% if tx\.status == \'Successful\' %}bg-green-100 text-green-800\s*{% elif tx\.status == \'Pending\' %}bg-yellow-100 text-yellow-800\s*{% else %}bg-red-100 text-red-800{% endif %}\">\s*{% if tx\.status == \'Successful\' %}\s*<svg class=\"w-4 h-4 mr-1\.5\" fill=\"currentColor\" viewBox=\"0 0 20 20\">\s*<path fill-rule=\"evenodd\"\s*d=\"M10 18a8 8 0 100-16 8 8 0 000 16zm3\.707-9\.293a1 1 0 00-1\.414-1\.414L9 10\.586 7\.707 9\.293a1 1 0 00-1\.414 1\.414l2 2a1 1 0 001\.414 0l4-4z\"\s*clip-rule=\"evenodd\"></path>\s*</svg>\s*{% endif %}\s*{{ tx\.status }}\s*</span>', re.DOTALL)

replacement = '''{% if tx.status == 'Pending' %}
                        <span class="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider print-exact bg-yellow-100 text-yellow-800">
                            Pending <span class="text-green-600 loading-dots mx-1 lowercase"></span> {{ tx.progress_percentage }}%
                        </span>
                        {% elif tx.status == 'Successful' %}
                        <span class="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider print-exact bg-green-100 text-green-800">
                            <svg class="w-4 h-4 mr-1.5" fill="currentColor" viewBox="0 0 20 20"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
                            Successful
                        </span>
                        {% else %}
                        <span class="inline-flex items-center px-4 py-1.5 rounded-full text-sm font-bold uppercase tracking-wider print-exact bg-red-100 text-red-800">
                            {{ tx.status }}
                        </span>
                        {% endif %}'''

content = pattern.sub(replacement, content)

with open('banking/templates/banking/receipt.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
