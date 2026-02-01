"""
Expense Tracker - Backend API
Arquitectura modular y segura
"""
import os
import sqlite3
from flask import Flask, jsonify
from flask_cors import CORS

# Importar rutas
from routes.auth import auth_bp
from routes.transactions import trans_bp

# Inicializar Flask
app = Flask(__name__)

# ==================== CONFIGURACIÓN DE SEGURIDAD ====================

# CORS con protección
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"],
        "max_age": 3600
    }
})

# Headers de seguridad
@app.after_request
def set_security_headers(response):
    """Agrega headers de seguridad a todas las respuestas"""
    # Prevenir clickjacking
    response.headers['X-Frame-Options'] = 'DENY'
    
    # Prevenir MIME sniffing
    response.headers['X-Content-Type-Options'] = 'nosniff'
    
    # Prevenir XSS
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self' data:"
    
    # HSTS
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    # Referrer Policy
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    
    return response

# ==================== INICIALIZACIÓN DE BASE DE DATOS ====================

def init_db():
    """Crea las tablas de la base de datos"""
    conn = sqlite3.connect('expenses.db')
    c = conn.cursor()
    
    # Tabla de usuarios
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            password_salt TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de transacciones
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY,
            user_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT,
            type TEXT DEFAULT 'expense',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# ==================== REGISTRO DE RUTAS ====================

# Rutas de autenticación
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Rutas de transacciones
app.register_blueprint(trans_bp, url_prefix='/api/transactions')

# ==================== MANEJO DE ERRORES ====================

@app.errorhandler(400)
def bad_request(error):
    """Manejo de errores 400"""
    return jsonify({'error': 'Solicitud inválida'}), 400

@app.errorhandler(404)
def not_found(error):
    """Manejo de errores 404"""
    return jsonify({'error': 'Recurso no encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Manejo de errores 405"""
    return jsonify({'error': 'Método no permitido'}), 405

@app.errorhandler(500)
def internal_error(error):
    """Manejo de errores 500"""
    return jsonify({'error': 'Error interno del servidor'}), 500

# ==================== HEALTHCHECK ====================

@app.route('/api/health', methods=['GET'])
def health():
    """Verifica estado del servidor"""
    return jsonify({'status': 'ok'}), 200

# ==================== INICIO ====================

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001, host='0.0.0.0')
