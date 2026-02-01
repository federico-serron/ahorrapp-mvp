/**
 * Componente de Transacciones
 */

import {
    createTransaction, getTransactions, updateTransaction,
    deleteTransaction, getStats
} from '../api/client.js';
import {
    validateDescription, validateAmount, ValidationError
} from '../utils/validator.js';
import { escapeHtml, sanitizeDescription, sanitizeAmount } from '../utils/sanitizer.js';

export class TransactionsComponent {
    constructor(userId) {
        this.userId = userId;
        this.transactions = [];
        this.editingId = null;
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Crear transacción
        document.getElementById('transactionForm').addEventListener('submit', (e) => this.handleCreate(e));
        
        // Modal de edición
        document.getElementById('editForm').addEventListener('submit', (e) => this.handleEdit(e));
        document.querySelector('.modal-close').addEventListener('click', () => this.closeModal());
    }
    
    async handleCreate(e) {
        e.preventDefault();
        
        try {
            const description = document.getElementById('description').value;
            const amount = document.getElementById('amount').value;
            
            // Validar
            validateDescription(description);
            validateAmount(amount);
            
            // Sanitizar
            const safeDesc = sanitizeDescription(description);
            const safeAmount = sanitizeAmount(amount);
            
            // Crear
            await createTransaction(this.userId, safeDesc, safeAmount);
            
            // Limpiar form
            document.getElementById('transactionForm').reset();
            
            // Recargar
            await this.refresh();
            
            this.showSuccess('✅ Transacción registrada!');
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    async handleEdit(e) {
        e.preventDefault();
        
        try {
            if (!this.editingId) return;
            
            const description = document.getElementById('editDescription').value;
            const amount = document.getElementById('editAmount').value;
            
            // Validar
            validateDescription(description);
            validateAmount(amount);
            
            // Sanitizar
            const safeDesc = sanitizeDescription(description);
            const safeAmount = sanitizeAmount(amount);
            
            // Actualizar
            await updateTransaction(this.editingId, this.userId, safeDesc, safeAmount);
            
            // Cerrar modal
            this.closeModal();
            
            // Recargar
            await this.refresh();
            
            this.showSuccess('✅ Transacción actualizada!');
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    async handleDelete() {
        if (!confirm('¿Eliminar esta transacción?')) return;
        
        try {
            if (!this.editingId) return;
            
            await deleteTransaction(this.editingId, this.userId);
            
            this.closeModal();
            await this.refresh();
            
            this.showSuccess('✅ Transacción eliminada!');
            
        } catch (error) {
            this.showError(error.message);
        }
    }
    
    openEditModal(id, description, amount) {
        this.editingId = id;
        document.getElementById('editDescription').value = escapeHtml(description);
        document.getElementById('editAmount').value = amount;
        document.getElementById('editModal').classList.add('show');
    }
    
    closeModal() {
        document.getElementById('editModal').classList.remove('show');
        this.editingId = null;
    }
    
    async refresh() {
        await this.loadTransactions();
        await this.loadStats();
    }
    
    async loadTransactions() {
        try {
            this.transactions = await getTransactions(this.userId);
            this.renderTransactions();
        } catch (error) {
            console.error('Error cargando transacciones:', error);
        }
    }
    
    async loadStats() {
        try {
            const stats = await getStats(this.userId);
            this.renderStats(stats);
        } catch (error) {
            console.error('Error cargando estadísticas:', error);
        }
    }
    
    renderTransactions() {
        const container = document.getElementById('transactionsList');
        
        if (this.transactions.length === 0) {
            container.innerHTML = '<p class="no-transactions">No hay transacciones</p>';
            return;
        }
        
        container.innerHTML = this.transactions.map(t => `
            <div class="transaction-item ${t.type}">
                <div class="transaction-header">
                    <div class="transaction-description">${escapeHtml(t.description)}</div>
                    <span class="transaction-category">${escapeHtml(t.category)}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div class="transaction-amount ${t.type}">
                        ${t.type === 'income' ? '+' : '-'}$${Math.abs(t.amount).toFixed(2)}
                    </div>
                    <button class="btn-small" onclick="
                        window.transactionsComponent.openEditModal(
                            ${t.id},
                            '${t.description.replace(/'/g, "\\'")}',
                            ${t.amount}
                        )
                    ">Editar</button>
                </div>
            </div>
        `).join('');
    }
    
    renderStats(stats) {
        document.getElementById('incomeTotal').textContent = `$${stats.total_income.toFixed(2)}`;
        document.getElementById('expenseTotal').textContent = `$${stats.total_expenses.toFixed(2)}`;
        document.getElementById('balanceTotal').textContent = `$${stats.balance.toFixed(2)}`;
        
        this.updateCharts(stats);
    }
    
    updateCharts(stats) {
        // Aquí irían las gráficas
        console.log('Stats actualizado:', stats);
    }
    
    showSuccess(message) {
        const msgDiv = document.getElementById('message');
        msgDiv.textContent = escapeHtml(message);
        msgDiv.className = 'message show success';
        
        setTimeout(() => msgDiv.classList.remove('show'), 3000);
    }
    
    showError(message) {
        const msgDiv = document.getElementById('message');
        msgDiv.textContent = escapeHtml(message);
        msgDiv.className = 'message show error';
    }
}
