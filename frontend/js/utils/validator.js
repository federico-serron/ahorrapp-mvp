/**
 * Módulo de validaciones del lado del cliente
 */

export class ValidationError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ValidationError';
    }
}

/**
 * Valida username
 * - 3-20 caracteres
 * - Solo alfanuméricos, guiones y guiones bajos
 */
export function validateUsername(username) {
    if (typeof username !== 'string' || username.trim().length === 0) {
        throw new ValidationError('Username no puede estar vacío');
    }
    
    username = username.trim();
    
    if (username.length < 3) {
        throw new ValidationError('Username debe tener al menos 3 caracteres');
    }
    
    if (username.length > 20) {
        throw new ValidationError('Username no puede exceder 20 caracteres');
    }
    
    if (!/^[a-z0-9_-]+$/i.test(username)) {
        throw new ValidationError('Username solo puede contener letras, números, guiones y guiones bajos');
    }
    
    return username.trim();
}

/**
 * Valida contraseña
 * - Mínimo 4 caracteres
 * - Máximo 128 caracteres
 */
export function validatePassword(password) {
    if (typeof password !== 'string') {
        throw new ValidationError('Contraseña inválida');
    }
    
    if (password.length < 4) {
        throw new ValidationError('Contraseña debe tener al menos 4 caracteres');
    }
    
    if (password.length > 128) {
        throw new ValidationError('Contraseña es demasiado larga');
    }
    
    return password;
}

/**
 * Valida descripción
 * - 1-500 caracteres
 */
export function validateDescription(description) {
    if (typeof description !== 'string' || description.trim().length === 0) {
        throw new ValidationError('Descripción no puede estar vacía');
    }
    
    const desc = description.trim();
    
    if (desc.length > 500) {
        throw new ValidationError('Descripción no puede exceder 500 caracteres');
    }
    
    return desc;
}

/**
 * Valida monto
 * - Debe ser número
 * - No puede ser cero
 * - Máximo 2 decimales
 */
export function validateAmount(amount) {
    const num = parseFloat(amount);
    
    if (isNaN(num)) {
        throw new ValidationError('Monto debe ser un número válido');
    }
    
    if (num === 0) {
        throw new ValidationError('Monto no puede ser cero');
    }
    
    if (Math.abs(num) > 1000000) {
        throw new ValidationError('Monto excede el límite permitido');
    }
    
    return Math.round(num * 100) / 100;
}

/**
 * Valida que el formulario tiene todos los campos requeridos
 */
export function validateForm(formData, requiredFields) {
    const missing = requiredFields.filter(field => !formData[field]);
    
    if (missing.length > 0) {
        throw new ValidationError(`Campos requeridos: ${missing.join(', ')}`);
    }
}
