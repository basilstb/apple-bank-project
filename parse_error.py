import re

with open('error.html', 'r', encoding='utf-16') as f:
    html = f.read()

match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE | re.DOTALL)
if match:
    print("Title:", match.group(1).strip())

match = re.search(r'<div id="summary">(.*?)</div>', html, re.IGNORECASE | re.DOTALL)
if match:
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', '', match.group(1))
    print("Summary:", text.strip())

match = re.search(r'<pre class="exception_value">(.*?)</pre>', html, re.IGNORECASE | re.DOTALL)
if match:
    print("Exception:", match.group(1).strip())
