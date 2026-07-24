import os
file_path = 'banking/templates/banking/receipt.html'
with open(file_path, 'r') as f:
    content = f.read()
content = content.replace('onclick="window.print()"', 'onclick="setTimeout(function(){ window.print(); }, 500);"')
with open(file_path, 'w') as f:
    f.write(content)
