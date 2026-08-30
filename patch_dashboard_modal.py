import re

def modify_dashboard():
    with open('banking/templates/banking/dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace the inline WhatsApp button
    inline_btn_pattern = r'<a href=\"https://wa\.me/447345851907\"[^>]*>.*?Contact Customer Service \(WhatsApp\).*?</a>'
    inline_btn_replacement = '''<button onclick="document.getElementById('customer-service-modal').classList.remove('hidden'); document.getElementById('customer-service-modal').classList.add('flex');"
          class="w-full bg-[#25D366] text-white py-2 rounded-lg font-label-md text-label-md hover:bg-[#20ba5a] transition-colors shadow-sm col-span-2 flex items-center justify-center gap-2">
          <span class="material-symbols-outlined text-[18px]" translate="no">support_agent</span>
          Contact Customer Service
        </button>'''
    content = re.sub(inline_btn_pattern, inline_btn_replacement, content, flags=re.DOTALL)

    # Replace the floating WhatsApp button
    floating_btn_pattern = r'<!-- Floating WhatsApp Button -->.*?</a>'
    floating_btn_replacement = '''<!-- Floating Customer Service Button -->
<button onclick="document.getElementById('customer-service-modal').classList.remove('hidden'); document.getElementById('customer-service-modal').classList.add('flex');"
  class="fixed bottom-6 right-6 z-50 bg-primary text-white p-4 rounded-full shadow-lg hover:bg-primary-container transition-all duration-300 flex items-center justify-center hover:scale-110 group"
  title="Contact Customer Service">
  <span class="material-symbols-outlined text-[24px]" translate="no">support_agent</span>
  <span
    class="max-w-0 overflow-hidden group-hover:max-w-xs group-hover:ml-2 transition-all duration-500 ease-in-out whitespace-nowrap text-sm font-bold">
    Contact Support
  </span>
</button>

<!-- Customer Service Modal -->
<div id="customer-service-modal" class="hidden fixed inset-0 bg-black/50 z-[60] items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-sm w-full p-6 shadow-2xl border border-gray-100 flex flex-col gap-4 relative">
        <div class="flex justify-between items-start">
            <h3 class="text-lg font-bold text-gray-900">Contact Support</h3>
            <button onclick="document.getElementById('customer-service-modal').classList.add('hidden'); document.getElementById('customer-service-modal').classList.remove('flex');" class="text-gray-400 hover:text-gray-600">
                <span class="material-symbols-outlined text-[18px]" translate="no">close</span>
            </button>
        </div>
        <p class="text-sm text-gray-600 mb-2">How would you like to contact us?</p>
        
        <a href="https://wa.me/447345851907" target="_blank" rel="noopener noreferrer"
            class="w-full bg-[#25D366] text-white py-3 px-4 rounded-xl font-bold text-sm hover:bg-[#20ba5a] transition-colors shadow-sm flex items-center gap-3">
            <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946C.06 5.348 5.397.01 12.008.01c3.202.001 6.212 1.246 8.477 3.514 2.266 2.268 3.507 5.28 3.505 8.484-.004 6.657-5.34 11.997-11.953 11.997-2.005-.001-3.973-.502-5.724-1.455L0 24zm6.59-4.846c1.6.95 3.188 1.449 4.825 1.451 5.436 0 9.86-4.413 9.863-9.864.001-2.641-1.024-5.124-2.888-6.991A9.782 9.782 0 0 0 12.008 1.24c-5.434 0-9.858 4.413-9.862 9.865-.001 1.739.461 3.43 1.337 4.937l-.989 3.612 3.701-.97c1.517.827 3.09 1.26 4.852 1.262zm9.733-7.224c-.269-.134-1.593-.786-1.839-.876-.246-.09-.425-.134-.604.134-.179.269-.694.876-.851 1.056-.157.179-.313.202-.582.067-.269-.134-1.137-.419-2.166-1.337-.801-.714-1.342-1.596-1.499-1.865-.157-.269-.017-.414.118-.548.121-.121.269-.314.403-.471.134-.157.179-.269.269-.449.09-.179.045-.336-.022-.471-.067-.134-.604-1.456-.827-1.994-.217-.523-.456-.452-.627-.461-.163-.008-.349-.01-.535-.01-.186 0-.49.07-.747.349-.257.279-.982.96-9.82.96s-1.066-.681-1.324-.96c-.257-.279-.49-.07-.747-.07-.257 0-.425.045-.604.179-.179.134-1.593 1.558-1.593 3.801 0 2.243 1.637 4.413 1.861 4.713.224.3 3.225 4.925 7.814 6.903 1.092.47 1.944.75 2.609.961 1.097.349 2.096.3 2.886.182.88-.132 2.707-1.106 3.088-2.122.381-1.016.381-1.886.269-2.065-.113-.179-.313-.269-.582-.403z" />
            </svg>
            WhatsApp
        </a>
        
        <a href="mailto:info@nexuscustomerservice.online" 
            class="w-full bg-blue-600 text-white py-3 px-4 rounded-xl font-bold text-sm hover:bg-blue-700 transition-colors shadow-sm flex items-center gap-3">
            <span class="material-symbols-outlined text-[20px]" translate="no">mail</span>
            Email Support
        </a>
    </div>
</div>
'''
    content = re.sub(floating_btn_pattern, floating_btn_replacement, content, flags=re.DOTALL)

    with open('banking/templates/banking/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)

modify_dashboard()
print('Dashboard modified')
