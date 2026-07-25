import sys
import re

# Update base.html
with open('templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

css_to_add = '''
        @keyframes loadingDots {
            0% { content: "."; }
            25% { content: ".."; }
            50% { content: "..."; }
            75% { content: "...."; }
            100% { content: "....."; }
        }
        .loading-dots::after {
            content: ".";
            animation: loadingDots 1.5s infinite steps(1);
            display: inline-block;
            width: 1.5em;
            text-align: left;
        }
    </style>'''

content = content.replace('    </style>', css_to_add, 1)

with open('templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Update history.html
with open('banking/templates/banking/history.html', 'r', encoding='utf-8') as f:
    content = f.read()

pattern = re.compile(r'<td class=\"px-6 py-4 whitespace-nowrap text-center\">\s*<span\s*class=\"px-2 inline-flex text-xs leading-5 font-semibold rounded-full {% if tx\.status == \'Successful\' %}bg-green-100 text-green-800{% elif tx\.status == \'Pending\' %}bg-yellow-100 text-yellow-800{% else %}bg-red-100 text-red-800{% endif %}\">\s*{{ tx\.status }}\s*</span>\s*</td>', re.DOTALL)

replacement = '''<td class="px-6 py-4 whitespace-nowrap text-center">
                        {% if tx.status == 'Pending' %}
                        <span class="px-3 py-1 inline-flex items-center text-xs leading-5 font-bold rounded-full bg-yellow-100 text-yellow-800">
                            Pending <span class="text-green-600 loading-dots mx-1"></span> {{ tx.progress_percentage }}%
                        </span>
                        {% elif tx.status == 'Successful' %}
                        <span class="px-3 py-1 inline-flex items-center text-xs leading-5 font-bold rounded-full bg-green-100 text-green-800">
                            Successful
                        </span>
                        {% else %}
                        <span class="px-3 py-1 inline-flex items-center text-xs leading-5 font-bold rounded-full bg-red-100 text-red-800">
                            {{ tx.status }}
                        </span>
                        {% endif %}
                    </td>'''

content = pattern.sub(replacement, content)

with open('banking/templates/banking/history.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Done!')
