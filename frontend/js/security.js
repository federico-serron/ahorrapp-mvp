/**
 * Módulo de seguridad - Sanitización y validación
 */

/**
 * Escapa caracteres HTML para evitar XSS
 */
function escapeHtml(text) {
    if (typeof text !== 'string') return '';
    
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    
    return text.replace(/[&<>"']/g, m => map[m]);
}

/**
 * Sanitiza input de usuario
 */
function sanitizeInput(value, maxLength = 255) {
    if (typeof value !== 'string') return '';
    
    // Remover caracteres de control
    value = value.replace(/[\x00-\x1f\x7f]/g, '');
    
    // Limitar longitud
    value = value.substring(0, maxLength);
    
    return value.trim();
}

/**
 * Valida username
 */
function validateUsername(username) {
    if (!username || typeof username !== 'string') {
        return { valid: false, error: 'Username requerido' };
    }
    
    username = username.trim();
    
    if (username.length < 3) {
        return { valid: false, error: 'Username debe tener al menos 3 caracteres' };
    }
    
    if (username.length > 20) {
        return { valid: false, error: 'Username máximo 20 caracteres' };
    }
    
    if (!/^[a-z0-9_-]+$/i.test(username)) {
        return { valid: false, error: 'Solo letras, números, guiones' };
    }
    
    return { valid: true };
}

/**
 * Valida contraseña
 */
function validatePassword(password) {
    if (!password || typeof password !== 'string') {
        return { valid: false, error: 'Password requerido' };
    }
    
    if (password.length < 4) {
        return { valid: false, error: 'Password mínimo 4 caracteres' };
    }
    
    if (password.length > 128) {
        return { valid: false, error: 'Password muy largo' };
    }
    
    return { valid: true };
}

/**
 * Valida descripción
 */
function validateDescription(desc) {
    if (!desc || typeof desc !== 'string') {
        return { valid: false, error: 'Descripción requerida' };
    }
    
    desc = desc.trim();
    
    if (desc.length < 1) {
        return { valid: false, error: 'Descripción no puede estar vacía' };
    }
    
    if (desc.length > 500) {
        return { valid: false, error: 'Descripción muy larga (máx 500)' };
    }
    
    return { valid: true };
}

/**
 * Valida monto
 */
function validateAmount(amount) {
    const num = parseFloat(amount);
    
    if (isNaN(num)) {
        return { valid: false, error: 'Monto debe ser un número' };
    }
    
    if (num === 0) {
        return { valid: false, error: 'Monto no puede ser cero' };
    }
    
    if (Math.abs(num) > 1000000) {
        return { valid: false, error: 'Monto excede límite permitido' };
    }
    
    return { valid: true, value: parseFloat(num.toFixed(2)) };
}

/**
 * Valida todo un formulario
 */
function validateFormData(formData, fields) {
    const errors = {};
    
    fields.forEach(field => {
        if (field.type === 'username') {
            const result = validateUsername(formData[field.name]);
            if (!result.valid) errors[field.name] = result.error;
        } else if (field.type === 'password') {
            const result = validatePassword(formData[field.name]);
            if (!result.valid) errors[field.name] = result.error;
        } else if (field.type === 'description') {
            const result = validateDescription(formData[field.name]);
            if (!result.valid) errors[field.name] = result.error;
        } else if (field.type === 'amount') {
            const result = validateAmount(formData[field.name]);
            if (!result.valid) errors[field.name] = result.error;
        }
    });
    
    return {
        valid: Object.keys(errors).length === 0,
        errors
    };
}

/**
 * Almacenamiento seguro en localStorage
 */
const SecureStorage = {
    set: function(key, value) {
        try {
            // Solo almacenar datos no sensibles
            if (key === 'user') {
                const safe = {
                    id: value.id,
                    username: escapeHtml(value.username),
                    token: value.token
                };
                localStorage.setItem(key, JSON.stringify(safe));
            } else {
                localStorage.setItem(key, JSON.stringify(value));
            }
        } catch (e) {
            console.error('Error guardando en localStorage:', e);
        }
    },
    
    get: function(key) {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : null;
        } catch (e) {
            console.error('Error leyendo localStorage:', e);
            return null;
        }
    },
    
    remove: function(key) {
        try {
            localStorage.removeItem(key);
        } catch (e) {
            console.error('Error eliminando de localStorage:', e);
        }
    }
};
