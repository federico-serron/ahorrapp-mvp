/**
 * Módulo de UI - Manejo de interfaz de usuario
 */

const UI = {
    /**
     * Muestra/oculta secciones
     */
    showAuthSection() {
        document.getElementById('authSection').classList.remove('hidden');
        document.getElementById('appSection').classList.add('hidden');
    },
    
    showAppSection(username) {
        document.getElementById('authSection').classList.add('hidden');
        document.getElementById('appSection').classList.remove('hidden');
        document.getElementById('userName').textContent = `Bienvenido, ${escapeHtml(username)}! 👋`;
    },
    
    /**
     * Manejo de tabs
     */
    switchTab(tab) {
        document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
        document.getElementById(tab + 'Form').classList.remove('hidden');
        
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.add('inactive');
            btn.classList.remove('active');
        });
        event.target.classList.remove('inactive');
        event.target.classList.add('active');
    },
    
    /**
     * Manejo de mensajes
     */
    showMessage(containerId, message, type = 'success') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        // Escapar HTML
        message = escapeHtml(message);
        
        container.textContent = message;
        container.className = `message show ${type}`;
        
        // Auto-desaparecer después de 3 segundos
        if (type === 'success') {
            setTimeout(() => {
                container.classList.remove('show');
            }, 3000);
        }
    },
    
    /**
     * Limpia formulario
     */
    clearForm(formId) {
        const form = document.getElementById(formId);
        if (form) form.reset();
    },
    
    /**
     * Renderiza lista de transacciones
     */
    renderTransactions(transactions) {
        const container = document.getElementById('transactionsList');
        
        if (!transactions || transactions.length === 0) {
            container.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No hay transacciones</p>';
            return;
        }
        
        container.innerHTML = transactions.map(t => `
            <div class="transaction-item ${t.type}">
                <div class="transaction-header">
                    <div class="transaction-description">${escapeHtml(t.description)}</div>
                    <span class="transaction-category">${escapeHtml(t.category)}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="transaction-amount ${t.type}">
                        ${t.type === 'income' ? '+' : '-'}$${Math.abs(t.amount).toFixed(2)}
                    </div>
                    <button class="btn-small" onclick="UI.openEditModal(${t.id}, '${escapeHtml(t.description)}', ${t.amount})">Editar</button>
                </div>
            </div>
        `).join('');
    },
    
    /**
     * Actualiza estadísticas
     */
    updateStats(stats) {
        document.getElementById('incomeTotal').textContent = `$${stats.total_income.toFixed(2)}`;
        document.getElementById('expenseTotal').textContent = `$${stats.total_expenses.toFixed(2)}`;
        document.getElementById('balanceTotal').textContent = `$${stats.balance.toFixed(2)}`;
    },
    
    /**
     * Modal de edición
     */
    openEditModal(id, description, amount) {
        window.editingTransactionId = id;
        document.getElementById('editDescription').value = description;
        document.getElementById('editAmount').value = amount;
        document.getElementById('editModal').classList.add('show');
    },
    
    closeEditModal() {
        document.getElementById('editModal').classList.remove('show');
        window.editingTransactionId = null;
    },
    
    /**
     * Disabilita/habilita botones
     */
    setButtonLoading(buttonId, loading = true) {
        const btn = document.getElementById(buttonId);
        if (!btn) return;
        
        if (loading) {
            btn.disabled = true;
            btn.dataset.originalText = btn.textContent;
            btn.textContent = 'Procesando...';
        } else {
            btn.disabled = false;
            btn.textContent = btn.dataset.originalText || btn.textContent;
        }
    }
};
