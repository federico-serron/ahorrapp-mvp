"""Seguridad - hashing y tokens"""
import hashlib
import secrets
import hmac

def hash_password(password, salt=None):
    """Hash seguro con salt usando PBKDF2"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000
    )
    return password_hash.hex(), salt

def verify_password(password, stored_hash, salt):
    """Verifica contraseña (constant-time comparison)"""
    password_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(password_hash, stored_hash)

def generate_token():
    """Token seguro aleatorio"""
    return secrets.token_hex(32)
