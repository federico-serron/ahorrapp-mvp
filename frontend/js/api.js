/**
 * Módulo de API - Llamadas seguras al backend
 */

const API = {
    baseURL: 'http://localhost:5001/api',
    timeout: 10000,
    
    /**
     * Realiza request HTTP seguro
     */
    async request(method, endpoint, data = null) {
        const url = `${this.baseURL}${endpoint}`;
        
        const options = {
            method,
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
            },
            timeout: this.timeout
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        try {
            const response = await fetch(url, options);
            const responseData = await response.json();
            
            return {
                ok: response.ok,
                status: response.status,
                data: responseData
            };
        } catch (error) {
            console.error('API Error:', error);
            return {
                ok: false,
                status: 0,
                data: { error: 'Error de conexión' }
            };
        }
    },
    
    /**
     * Autenticación - Registro
     */
    auth: {
        async register(username, password) {
            return API.request('POST', '/auth/register', { username, password });
        },
        
        async login(username, password) {
            return API.request('POST', '/auth/login', { username, password });
        }
    },
    
    /**
     * Transacciones
     */
    transactions: {
        async create(userId, description, amount) {
            return API.request('POST', '/transactions', {
                user_id: userId,
                description,
                amount
            });
        },
        
        async getAll(userId) {
            return API.request('GET', `/transactions?user_id=${encodeURIComponent(userId)}`);
        },
        
        async update(transactionId, userId, description, amount) {
            return API.request('PUT', `/transactions/${transactionId}`, {
                user_id: userId,
                description,
                amount
            });
        },
        
        async delete(transactionId, userId) {
            return API.request('DELETE', `/transactions/${transactionId}`, {
                user_id: userId
            });
        }
    },
    
    /**
     * Estadísticas
     */
    stats: {
        async get(userId) {
            return API.request('GET', `/stats?user_id=${encodeURIComponent(userId)}`);
        }
    }
};
