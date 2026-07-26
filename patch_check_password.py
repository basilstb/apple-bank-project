import os

file_path = 'banking/views.py'
with open(file_path, 'r') as f:
    content = f.read()

old_code = """            is_valid_pin = False
            if sender_profile.transaction_pin == pin:
                is_valid_pin = True
                sender_profile.transaction_pin = make_password(pin)
                sender_profile.save(update_fields=['transaction_pin'])
            elif check_password(pin, sender_profile.transaction_pin):
                is_valid_pin = True"""

new_code = """            is_valid_pin = False
            if sender_profile.transaction_pin == pin:
                is_valid_pin = True
                sender_profile.transaction_pin = make_password(pin)
                sender_profile.save(update_fields=['transaction_pin'])
            elif sender_profile.transaction_pin and check_password(pin, sender_profile.transaction_pin):
                is_valid_pin = True"""

content = content.replace(old_code, new_code)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched views.py for check_password")
