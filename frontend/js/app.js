/**
 * Módulo principal de la aplicación
 */

let currentUser = null;
let transactions = [];
let stats = null;
let categoryChart = null;
let incomeExpenseChart = null;

/**
 * Inicializa la aplicación
 */
function initApp() {
    // Verificar si hay usuario guardado
    const savedUser = SecureStorage.get('user');
    if (savedUser) {
        currentUser = savedUser;
        loadAppData();
        UI.showAppSection(currentUser.username);
    } else {
        UI.showAuthSection();
    }
    
    // Registrar event listeners
    registerEventListeners();
}

/**
 * Registra todos los event listeners
 */
function registerEventListeners() {
    // Auth
    document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
    document.getElementById('registerForm')?.addEventListener('submit', handleRegister);
    
    // Transacciones
    document.getElementById('transactionForm')?.addEventListener('submit', handleAddTransaction);
    document.getElementById('editForm')?.addEventListener('submit', handleEditTransaction);
}

/**
 * ============ AUTENTICACIÓN ============
 */

async function handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    const msgDiv = document.getElementById('loginMessage');
    
    // Validar
    const validation = validateFormData(
        { username, password },
        [
            { name: 'username', type: 'username' },
            { name: 'password', type: 'password' }
        ]
    );
    
    if (!validation.valid) {
        const error = Object.values(validation.errors)[0];
        UI.showMessage('loginMessage', error, 'error');
        return;
    }
    
    UI.setButtonLoading('loginBtn', true);
    
    const response = await API.auth.login(username, password);
    
    if (response.ok) {
        currentUser = response.data;
        SecureStorage.set('user', currentUser);
        
        UI.clearForm('loginForm');
        loadAppData();
        UI.showAppSection(currentUser.username);
    } else {
        UI.showMessage('loginMessage', response.data.error || 'Error en login', 'error');
    }
    
    UI.setButtonLoading('loginBtn', false);
}

async function handleRegister(e) {
    e.preventDefault();
    
    const username = document.getElementById('regUsername').value;
    const password = document.getElementById('regPassword').value;
    
    // Validar
    const validation = validateFormData(
        { username, password },
        [
            { name: 'username', type: 'username' },
            { name: 'password', type: 'password' }
        ]
    );
    
    if (!validation.valid) {
        const error = Object.values(validation.errors)[0];
        UI.showMessage('registerMessage', error, 'error');
        return;
    }
    
    UI.setButtonLoading('registerBtn', true);
    
    const response = await API.auth.register(username, password);
    
    if (response.ok) {
        UI.showMessage('registerMessage', 'Usuario creado! Inicia sesión', 'success');
        UI.clearForm('registerForm');
        setTimeout(() => UI.switchTab('login'), 1500);
    } else {
        UI.showMessage('registerMessage', response.data.error || 'Error en registro', 'error');
    }
    
    UI.setButtonLoading('registerBtn', false);
}

function logout() {
    if (!confirm('¿Cerrar sesión?')) return;
    
    currentUser = null;
    transactions = [];
    stats = null;
    
    SecureStorage.remove('user');
    UI.clearForm('loginForm');
    UI.clearForm('registerForm');
    UI.clearForm('transactionForm');
    UI.showAuthSection();
}

/**
 * ============ TRANSACCIONES ============
 */

async function handleAddTransaction(e) {
    e.preventDefault();
    
    const description = document.getElementById('description').value;
    const amount = document.getElementById('amount').value;
    
    // Validar
    const validation = validateFormData(
        { description, amount },
        [
            { name: 'description', type: 'description' },
            { name: 'amount', type: 'amount' }
        ]
    );
    
    if (!validation.valid) {
        const error = Object.values(validation.errors)[0];
        UI.showMessage('message', error, 'error');
        return;
    }
    
    // Obtener valor validado
    const amountResult = validateAmount(amount);
    
    UI.setButtonLoading('submitBtn', true);
    
    const response = await API.transactions.create(
        currentUser.id,
        description,
        amountResult.value
    );
    
    if (response.ok) {
        UI.showMessage('message', '✅ Transacción registrada!', 'success');
        UI.clearForm('transactionForm');
        await loadAppData();
    } else {
        UI.showMessage('message', response.data.error || 'Error al registrar', 'error');
    }
    
    UI.setButtonLoading('submitBtn', false);
}

async function handleEditTransaction(e) {
    e.preventDefault();
    
    const description = document.getElementById('editDescription').value;
    const amount = document.getElementById('editAmount').value;
    
    // Validar
    const validation = validateFormData(
        { description, amount },
        [
            { name: 'description', type: 'description' },
            { name: 'amount', type: 'amount' }
        ]
    );
    
    if (!validation.valid) {
        const error = Object.values(validation.errors)[0];
        alert(error);
        return;
    }
    
    const amountResult = validateAmount(amount);
    
    const response = await API.transactions.update(
        window.editingTransactionId,
        currentUser.id,
        description,
        amountResult.value
    );
    
    if (response.ok) {
        UI.closeEditModal();
        await loadAppData();
    } else {
        alert(response.data.error || 'Error al actualizar');
    }
}

async function deleteTransaction() {
    if (!confirm('¿Eliminar transacción?')) return;
    
    const response = await API.transactions.delete(
        window.editingTransactionId,
        currentUser.id
    );
    
    if (response.ok) {
        UI.closeEditModal();
        await loadAppData();
    } else {
        alert(response.data.error || 'Error al eliminar');
    }
}

/**
 * ============ CARGA DE DATOS ============
 */

async function loadAppData() {
    // Cargar transacciones
    const transResponse = await API.transactions.getAll(currentUser.id);
    if (transResponse.ok) {
        transactions = transResponse.data;
        UI.renderTransactions(transactions);
    }
    
    // Cargar estadísticas
    const statsResponse = await API.stats.get(currentUser.id);
    if (statsResponse.ok) {
        stats = statsResponse.data;
        UI.updateStats(stats);
        updateCharts(stats);
    }
}

/**
 * ============ GRÁFICAS ============
 */

function updateCharts(statsData) {
    if (!statsData.by_category) return;
    
    const categoryLabels = statsData.by_category.map(c => c.category);
    const categoryData = statsData.by_category.map(c => c.total);
    
    // Gráfica de categorías
    if (categoryChart) categoryChart.destroy();
    const ctxCategory = document.getElementById('categoryChart')?.getContext('2d');
    if (ctxCategory) {
        categoryChart = new Chart(ctxCategory, {
            type: 'doughnut',
            data: {
                labels: categoryLabels,
                datasets: [{
                    data: categoryData,
                    backgroundColor: [
                        '#667eea', '#764ba2', '#f093fb', '#4facfe',
                        '#00f2fe', '#4caf50', '#ff9800', '#f44336'
                    ]
                }]
            },
            options: { responsive: true, maintainAspectRatio: false }
        });
    }
    
    // Gráfica de ingresos vs gastos
    if (incomeExpenseChart) incomeExpenseChart.destroy();
    const ctxIncome = document.getElementById('incomeExpenseChart')?.getContext('2d');
    if (ctxIncome) {
        incomeExpenseChart = new Chart(ctxIncome, {
            type: 'bar',
            data: {
                labels: ['Ingresos', 'Gastos'],
                datasets: [{
                    label: 'Cantidad',
                    data: [statsData.total_income, statsData.total_expenses],
                    backgroundColor: ['#4caf50', '#f44336']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: { y: { beginAtZero: true } }
            }
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', initApp);
