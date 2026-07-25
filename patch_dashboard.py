import os

dashboard_path = "banking/templates/banking/dashboard.html"
with open(dashboard_path, 'r', encoding='utf-8') as f:
    content = f.read()

dashboard_old = """    <div class="md:col-span-8 bg-surface-container-lowest rounded-xl p-6 border border-slate-200 shadow-[0_4px_20px_-2px_rgba(0,0,0,0.04)] flex flex-col justify-between">
      <div>
        <div class="flex justify-between items-start mb-6">"""

dashboard_new = """    <div class="md:col-span-8 bg-surface-container-lowest rounded-xl p-6 border border-slate-200 shadow-[0_4px_20px_-2px_rgba(0,0,0,0.04)] flex flex-col justify-between">
      <div>
        <!-- Pending Transactions Section -->
        {% if pending_transactions %}
        <div class="mb-8">
            <h3 class="font-label-md text-label-md text-on-surface-variant uppercase tracking-wider mb-4">Pending Transactions</h3>
            <div class="space-y-4">
                {% for tx in pending_transactions %}
                <div class="bg-white rounded-xl p-4 shadow-sm border border-orange-200 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div class="flex items-center gap-4">
                        <div class="w-10 h-10 rounded-full bg-orange-100 text-orange-600 flex items-center justify-center shrink-0">
                            <span class="material-symbols-outlined">pending_actions</span>
                        </div>
                        <div>
                            <p class="font-bold text-on-surface">{{ tx.description }}</p>
                            <p class="text-sm text-on-surface-variant">{{ tx.timestamp|date:"M d, Y" }}</p>
                            {% if tx.pending_reason %}
                            <div class="mt-2 p-3 bg-orange-50 border border-orange-100 rounded-lg text-sm text-orange-800 flex items-start gap-2">
                                <span class="material-symbols-outlined text-[18px] shrink-0 mt-0.5">info</span>
                                <p><strong>Admin Note:</strong> {{ tx.pending_reason }}</p>
                            </div>
                            {% endif %}
                        </div>
                    </div>
                    <div class="text-right shrink-0">
                        <p class="font-bold text-orange-600">
                            {% if tx.sender == profile %}-{% else %}+{% endif %}{{ profile.currency }}{{ tx.amount|intcomma }}
                        </p>
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-orange-100 text-orange-800">
                            Pending ({{ tx.progress_percentage }}%)
                        </span>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}

        <div class="flex justify-between items-start mb-6">"""

content = content.replace(dashboard_old, dashboard_new)
with open(dashboard_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully patched dashboard.html")
