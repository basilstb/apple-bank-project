import os

file_path = 'banking/views.py'
with open(file_path, 'r') as f:
    content = f.read()

old_transfer_view = """@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            request.session['pending_transfer_data'] = form.cleaned_data
            request.session['pending_transfer_data']['amount'] = str(form.cleaned_data['amount'])
            return redirect('transfer_pin_verify')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})"""

new_transfer_view = """@login_required
@ratelimit(key='user', rate='3/m', block=True)
def transfer_view(request):
    if request.method == 'POST':
        form = TransferForm(request.POST)
        if form.is_valid():
            transfer_data = {
                'amount': str(form.cleaned_data['amount']),
                'recipient_account': str(form.cleaned_data['recipient_account']),
                'account_name': str(form.cleaned_data['account_name']),
                'bank_name': str(form.cleaned_data['bank_name']),
                'swift_code': str(form.cleaned_data.get('swift_code', '')),
                'ifsc_code': str(form.cleaned_data.get('ifsc_code', '')),
                'description': str(form.cleaned_data.get('description', '')),
            }
            request.session['pending_transfer_data'] = transfer_data
            request.session.modified = True
            return redirect('transfer_pin_verify')
    else:
        form = TransferForm()
    return render(request, 'banking/transfer.html', {'form': form})"""

content = content.replace(old_transfer_view, new_transfer_view)

old_render = """    return render(request, 'banking/transfer_pin.html', {
        'form': form,
        'transfer_data': transfer_data
    })"""

new_render = """    context_data = transfer_data.copy()
    try:
        context_data['amount'] = float(transfer_data['amount'])
    except (ValueError, TypeError):
        pass
        
    return render(request, 'banking/transfer_pin.html', {
        'form': form,
        'transfer_data': context_data
    })"""

content = content.replace(old_render, new_render)

with open(file_path, 'w') as f:
    f.write(content)

print("Patched views.py")
