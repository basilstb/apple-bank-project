import os

file_path = 'banking/templates/banking/receipt.html'
with open(file_path, 'r') as f:
    content = f.read()

# 1. Change the button to Download Receipt
old_button = '''<button onclick="downloadPDF()"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-apple-dark transition-colors">
                <svg class="-ml-1 mr-2 h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4">
                    </path>
                </svg>
                Download PDF
            </button>'''

new_button = '''<button onclick="downloadReceipt()"
                class="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-apple-dark transition-colors">
                <svg class="-ml-1 mr-2 h-5 w-5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4">
                    </path>
                </svg>
                Download Receipt
            </button>'''

content = content.replace(old_button, new_button)

# 2. Replace html2pdf script with html2canvas script
old_script = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>
<script>
    function downloadPDF() {
        const element = document.getElementById('receipt-content');
        const opt = {
            margin:       0.5,
            filename:     'receipt_TXN-{{ tx.id|stringformat:"06d" }}.pdf',
            image:        { type: 'jpeg', quality: 0.98 },
            html2canvas:  { scale: 2, useCORS: true },
            jsPDF:        { unit: 'in', format: 'letter', orientation: 'portrait' }
        };
        html2pdf().set(opt).from(element).save();
    }
</script>'''

new_script = '''<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
<script>
    function downloadReceipt() {
        const element = document.getElementById('receipt-content');
        html2canvas(element, { scale: 2, useCORS: true, backgroundColor: '#ffffff' }).then(canvas => {
            const link = document.createElement('a');
            link.download = 'receipt_TXN-{{ tx.id|stringformat:"06d" }}.jpg';
            link.href = canvas.toDataURL('image/jpeg', 0.98);
            link.click();
        });
    }
</script>'''

content = content.replace(old_script, new_script)

# Also remove html2pdf from header if it's there
header_script = '<script src="https://cdnjs.cloudflare.com/ajax/libs/html2pdf.js/0.10.1/html2pdf.bundle.min.js"></script>'
content = content.replace(header_script, '')

with open(file_path, 'w') as f:
    f.write(content)
