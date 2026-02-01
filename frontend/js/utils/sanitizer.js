/**
 * Módulo de sanitización - Previene XSS y otros ataques
 */

/**
 * Escapa caracteres HTML peligrosos
 */
export function escapeHtml(text) {
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
 * Valida y sanitiza email
 */
export function sanitizeEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) ? email.trim() : '';
}

/**
 * Sanitiza username - solo alfanuméricos, guiones, guiones bajos
 */
export function sanitizeUsername(username) {
    if (typeof username !== 'string') return '';
    
    return username
        .trim()
        .toLowerCase()
        .replace(/[^a-z0-9_-]/g, '')
        .slice(0, 20);
}

/**
 * Sanitiza descripción - permite más caracteres pero escapa HTML
 */
export function sanitizeDescription(description) {
    if (typeof description !== 'string') return '';
    
    return escapeHtml(description.trim()).slice(0, 500);
}

/**
 * Sanitiza cantidad - solo números y punto decimal
 */
export function sanitizeAmount(amount) {
    if (typeof amount === 'string') {
        amount = parseFloat(amount);
    }
    
    // Validar que es número
    if (isNaN(amount)) return 0;
    
    // Redondear a 2 decimales
    return Math.round(amount * 100) / 100;
}

/**
 * Previene inyección de atributos
 */
export function sanitizeAttribute(attr) {
    if (typeof attr !== 'string') return '';
    
    return attr
        .replace(/[<>'"]/g, '')
        .trim()
        .slice(0, 255);
}
