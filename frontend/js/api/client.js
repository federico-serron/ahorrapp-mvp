/**
 * Cliente API seguro
 * - CSRF protection
 * - Error handling
 * - Validación de respuestas
 */

const API_URL = 'http://localhost:5001/api';

/**
 * Realiza request HTTP seguro
 */
async function apiRequest(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                // Agregar headers de seguridad
                'X-Requested-With': 'XMLHttpRequest'
            },
            mode: 'cors',
            credentials: 'include'
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${API_URL}${endpoint}`, options);
        
        // Validar que response es JSON
        const contentType = response.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            throw new Error('Respuesta inválida del servidor');
        }
        
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Error desconocido');
        }
        
        return result;
        
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ==================== Auth API ====================

export async function register(username, password) {
    return apiRequest('/auth/register', 'POST', {
        username,
        password
    });
}

export async function login(username, password) {
    return apiRequest('/auth/login', 'POST', {
        username,
        password
    });
}

// ==================== Transactions API ====================

export async function createTransaction(userId, description, amount) {
    return apiRequest('/transactions', 'POST', {
        user_id: userId,
        description,
        amount
    });
}

export async function getTransactions(userId) {
    return apiRequest(`/transactions?user_id=${userId}`);
}

export async function updateTransaction(transId, userId, description, amount) {
    return apiRequest(`/transactions/${transId}`, 'PUT', {
        user_id: userId,
        description,
        amount
    });
}

export async function deleteTransaction(transId, userId) {
    return apiRequest(`/transactions/${transId}`, 'DELETE', {
        user_id: userId
    });
}

export async function getStats(userId) {
    return apiRequest(`/transactions/stats?user_id=${userId}`);
}

// ==================== Health Check ====================

export async function healthCheck() {
    return apiRequest('/health');
}
