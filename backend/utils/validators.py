"""Validaciones y sanitización de entradas"""
import re

class ValidationError(Exception):
    pass

def sanitize_string(value, max_length=255):
    """Sanitiza string: elimina caracteres peligrosos"""
    if not isinstance(value, str):
        raise ValidationError("Debe ser texto")
    
    value = value.strip()
    if not value or len(value) > max_length:
        raise ValidationError(f"Texto inválido (máx {max_length})")
    
    # Remover caracteres de control
    value = re.sub(r'[\x00-\x1f\x7f]', '', value)
    return value

def validate_username(username):
    """Valida username: 3-20 chars, solo alfanuméricos/guiones"""
    username = sanitize_string(username, 20).lower()
    
    if len(username) < 3:
        raise ValidationError("Username mín 3 caracteres")
    
    if not re.match(r'^[a-z0-9_-]+$', username):
        raise ValidationError("Solo letras, números, guiones")
    
    return username

def validate_password(password):
    """Valida password: mín 4 caracteres"""
    if not isinstance(password, str) or len(password) < 4:
        raise ValidationError("Password mín 4 caracteres")
    return password

def validate_amount(amount):
    """Valida monto: número, no cero"""
    try:
        amount = float(amount)
        if amount == 0:
            raise ValidationError("Monto no puede ser cero")
        if abs(amount) > 1000000:
            raise ValidationError("Monto muy grande")
        return round(amount, 2)
    except (ValueError, TypeError):
        raise ValidationError("Monto debe ser número")

def validate_description(description):
    """Valida descripción"""
    return sanitize_string(description, 500)
