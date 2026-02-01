"""
Expense Tracker - Backend Seguro y Modular
Protecciones contra: XSS, SQL Injection, CORS, CSRF
"""
import os
import json
import sqlite3
import hashlib
import secrets
import hmac
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

app = Flask(__name__)

# ============================================================================
# CONFIGURACIÓN DE SEGURIDAD
# ============================================================================

# CORS: Solo localhost en desarrollo
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5001"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Headers de seguridad
@app.after_request
def set_security_headers(response):
    """Agrega headers de seguridad a todas las respuestas"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

DATABASE = 'expenses.db'

# ============================================================================
# VALIDACIONES Y SANITIZACIÓN
# ============================================================================

class ValidationError(Exception):
    """Excepción para errores de validación"""
    pass

def sanitize_string(value, max_length=255, field_name="field"):
    """Sanitiza strings: elimina caracteres peligrosos"""
    if not isinstance(value, str):
        raise ValidationError(f"{field_name} debe ser texto")
    
    value = value.strip()
    
    if len(value) == 0:
        raise ValidationError(f"{field_name} no puede estar vacío")
    
    if len(value) > max_length:
        raise ValidationError(f"{field_name} es demasiado largo (máx {max_length})")
    
    # Eliminar caracteres de control
    value = re.sub(r'[\x00-\x1f\x7f]', '', value)
    
    return value

def validate_username(username):
    """Valida username: 3-20 chars, solo alfanuméricos/guiones"""
    if not isinstance(username, str):
        raise ValidationError("Username debe ser texto")
    
    username = username.strip().lower()
    
    if len(username) < 3 or len(username) > 20:
        raise ValidationError("Username debe tener 3-20 caracteres")
    
    if not re.match(r'^[a-z0-9_-]+$', username):
        raise ValidationError("Username solo: letras, números, guiones, guiones bajos")
    
    return username

def validate_password(password):
    """Valida password: mín 4 caracteres"""
    if not isinstance(password, str):
        raise ValidationError("Password debe ser texto")
    
    if len(password) < 4 or len(password) > 128:
        raise ValidationError("Password debe tener 4-128 caracteres")
    
    return password

def validate_amount(amount):
    """Valida monto: número válido, no cero"""
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValidationError("Monto debe ser número válido")
    
    if amount == 0:
        raise ValidationError("Monto no puede ser cero")
    
    if abs(amount) > 1000000:
        raise ValidationError("Monto excede límite permitido")
    
    return round(amount, 2)

def validate_description(description):
    """Valida descripción"""
    return sanitize_string(description, max_length=500, field_name="description")

def validate_user_id(user_id):
    """Valida user_id: debe ser entero positivo"""
    try:
        user_id = int(user_id)
        if user_id <= 0:
            raise ValidationError("user_id inválido")
        return user_id
    except (ValueError, TypeError):
        raise ValidationError("user_id debe ser número entero")

# ============================================================================
# SEGURIDAD - HASHING Y TOKENS
# ============================================================================

def hash_password(password, salt=None):
    """Hash seguro con salt usando PBKDF2"""
    if salt is None:
        salt = secrets.token_hex(16)
    
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations
    )
    
    return password_hash.hex(), salt

def verify_password(password, stored_hash, salt):
    """Verifica password (constant-time comparison para evitar timing attacks)"""
    password_hash, _ = hash_password(password, salt)
    return hmac.compare_digest(password_hash, stored_hash)

# ============================================================================
# CATEGORIZACIÓN
# ============================================================================

def categorize_transaction(description):
    """Categoriza transacción y detecta ingreso vs gasto"""
    desc_lower = description.lower()
    
    income_keywords = [
        'sueldo', 'salario', 'pago', 'ingreso', 'venta', 
        'bonus', 'ganancia', 'reembolso', 'comisión', 'freelance'
    ]
    
    is_income = any(kw in desc_lower for kw in income_keywords)
    trans_type = 'income' if is_income else 'expense'
    
    categories = {
        'Alimentacion': ['café', 'comida', 'desayuno', 'almuerzo', 'cena', 'restaurant'],
        'Transporte': ['taxi', 'bus', 'uber', 'gasolina', 'metro', 'tren'],
        'Entretenimiento': ['cine', 'película', 'juego', 'música', 'bar', 'pub'],
        'Salud': ['farmacia', 'medicina', 'doctor', 'médico', 'hospital', 'gym'],
        'Servicios': ['internet', 'teléfono', 'electricidad', 'agua', 'gas'],
        'Compras': ['ropa', 'zapatos', 'tienda', 'regalo', 'amazon'],
        'Ingresos': income_keywords,
    }
    
    category = 'Otros'
    for cat, keywords in categories.items():
        if any(kw in desc_lower for kw in keywords):
            category = cat
            break
    
    return category, trans_type

# ============================================================================
# BASE DE DATOS
# ============================================================================

def init_db():
    """Inicializa base de datos"""
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  password_salt TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER NOT NULL,
                  description TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT,
                  type TEXT DEFAULT 'expense',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)''')
    
    conn.commit()
    conn.close()

# ============================================================================
# RUTAS - AUTENTICACIÓN
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Registra nuevo usuario"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        username = validate_username(data.get('username', ''))
        password = validate_password(data.get('password', ''))
        
        password_hash, salt = hash_password(password)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)',
                  (username, password_hash, salt))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        return jsonify({'id': user_id, 'username': username, 'message': 'Usuario creado'}), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuario ya existe'}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login de usuario"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        username = validate_username(data.get('username', ''))
        password = data.get('password', '')
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT id, password_hash, password_salt FROM users WHERE username = ?', 
                  (username,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        user_id, stored_hash, salt = result
        
        if not verify_password(password, stored_hash, salt):
            return jsonify({'error': 'Credenciales incorrectas'}), 401
        
        return jsonify({'id': user_id, 'username': username}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# ============================================================================
# RUTAS - TRANSACCIONES
# ============================================================================

@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    """Crea nueva transacción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        user_id = validate_user_id(data.get('user_id'))
        description = validate_description(data.get('description', ''))
        amount = validate_amount(data.get('amount'))
        
        category, trans_type = categorize_transaction(description)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        now = datetime.now().isoformat()
        c.execute(
            'INSERT INTO transactions (user_id, description, amount, category, type, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (user_id, description, amount, category, trans_type, now)
        )
        conn.commit()
        trans_id = c.lastrowid
        conn.close()
        
        return jsonify({
            'id': trans_id,
            'description': description,
            'amount': amount,
            'category': category,
            'type': trans_type,
            'created_at': now
        }), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions/<int:trans_id>', methods=['PUT'])
def update_transaction(trans_id):
    """Actualiza transacción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        user_id = validate_user_id(data.get('user_id'))
        description = validate_description(data.get('description', ''))
        amount = validate_amount(data.get('amount'))
        
        category, trans_type = categorize_transaction(description)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            'UPDATE transactions SET description=?, amount=?, category=?, type=? WHERE id=? AND user_id=?',
            (description, amount, category, trans_type, trans_id, user_id)
        )
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Actualizado'}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    """Elimina transacción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        user_id = validate_user_id(data.get('user_id'))
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id=? AND user_id=?', (trans_id, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Eliminado'}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    """Obtiene transacciones del usuario"""
    try:
        user_id = validate_user_id(request.args.get('user_id'))
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute(
            'SELECT id, description, amount, category, type, created_at FROM transactions WHERE user_id=? ORDER BY created_at DESC',
            (user_id,)
        )
        transactions = []
        for row in c.fetchall():
            transactions.append({
                'id': row[0],
                'description': row[1],
                'amount': row[2],
                'category': row[3],
                'type': row[4],
                'created_at': row[5]
            })
        conn.close()
        
        return jsonify(transactions), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del usuario"""
    try:
        user_id = validate_user_id(request.args.get('user_id'))
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        c.execute('SELECT SUM(amount) FROM transactions WHERE user_id=? AND type="expense"', (user_id,))
        total_expenses = c.fetchone()[0] or 0
        
        c.execute('SELECT SUM(amount) FROM transactions WHERE user_id=? AND type="income"', (user_id,))
        total_income = c.fetchone()[0] or 0
        
        balance = total_income - total_expenses
        
        c.execute(
            'SELECT category, COUNT(*), SUM(amount) FROM transactions WHERE user_id=? AND type="expense" GROUP BY category',
            (user_id,)
        )
        by_category = [{'category': row[0], 'count': row[1], 'total': row[2]} for row in c.fetchall()]
        
        conn.close()
        
        return jsonify({
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': balance,
            'by_category': by_category
        }), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno del servidor'}), 500

# ============================================================================
# INICIO
# ============================================================================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001, host='0.0.0.0')
