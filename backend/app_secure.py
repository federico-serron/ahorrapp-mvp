"""
Expense Tracker - Backend Seguro
Aplicación Flask con protecciones contra ataques comunes
"""
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Imports locales
from db.models import init_db, User, Transaction
from utils.validators import (
    ValidationError, validate_username, validate_password,
    validate_description, validate_amount, validate_user_id, validate_transaction_id
)
from utils.categorizer import categorize_transaction
from utils.security import generate_token

# Inicializar Flask
app = Flask(__name__)

# Configuración de CORS - SEGURO
# Solo permitir requests desde localhost en desarrollo
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000", "http://localhost:*"],
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "max_age": 3600,
         "supports_credentials": False
     }})

# Headers de seguridad
@app.after_request
def set_security_headers(response):
    """Agrega headers de seguridad"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
    return response

# Inicializar DB
init_db()

# ============ RUTAS DE AUTENTICACIÓN ============

@app.route('/api/auth/register', methods=['POST', 'OPTIONS'])
def register():
    """
    Registra nuevo usuario
    POST /api/auth/register
    Body: {username, password}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Body debe ser JSON'}), 400
        
        # Validar entrada
        username = validate_username(data.get('username', ''))
        password = validate_password(data.get('password', ''))
        
        # Crear usuario
        user_id = User.create(username, password)
        
        if not user_id:
            return jsonify({'error': 'Usuario ya existe'}), 409
        
        return jsonify({
            'id': user_id,
            'username': username,
            'message': 'Usuario creado exitosamente'
        }), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/auth/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Login de usuario
    POST /api/auth/login
    Body: {username, password}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Body debe ser JSON'}), 400
        
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return jsonify({'error': 'Username y password requeridos'}), 400
        
        # Autenticar
        user = User.authenticate(username, password)
        
        if not user:
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        # Generar token
        token = generate_token()
        
        return jsonify({
            'id': user['id'],
            'username': user['username'],
            'token': token
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ============ RUTAS DE TRANSACCIONES ============

@app.route('/api/transactions', methods=['POST', 'OPTIONS'])
def add_transaction():
    """
    Crea nueva transacción
    POST /api/transactions
    Body: {user_id, description, amount}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Body debe ser JSON'}), 400
        
        # Validar entrada
        user_id = validate_user_id(data.get('user_id'))
        description = validate_description(data.get('description', ''))
        amount = validate_amount(data.get('amount', 0))
        
        # Categorizar
        category, trans_type = categorize_transaction(description)
        
        # Crear transacción
        trans_id = Transaction.create(user_id, description, amount, category, trans_type)
        
        if not trans_id:
            return jsonify({'error': 'Error al crear transacción'}), 500
        
        return jsonify({
            'id': trans_id,
            'description': description,
            'amount': amount,
            'category': category,
            'type': trans_type,
            'created_at': datetime.now().isoformat()
        }), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al crear transacción: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions/<int:trans_id>', methods=['PUT', 'OPTIONS'])
def update_transaction(trans_id):
    """
    Actualiza transacción
    PUT /api/transactions/<id>
    Body: {user_id, description, amount}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Body debe ser JSON'}), 400
        
        # Validar entrada
        trans_id = validate_transaction_id(trans_id)
        user_id = validate_user_id(data.get('user_id'))
        description = validate_description(data.get('description', ''))
        amount = validate_amount(data.get('amount', 0))
        
        # Categorizar
        category, trans_type = categorize_transaction(description)
        
        # Actualizar
        success = Transaction.update(trans_id, user_id, description, amount, category, trans_type)
        
        if not success:
            return jsonify({'error': 'Transacción no encontrada o acceso denegado'}), 404
        
        return jsonify({'message': 'Transacción actualizada'}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar transacción: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions/<int:trans_id>', methods=['DELETE', 'OPTIONS'])
def delete_transaction(trans_id):
    """
    Elimina transacción
    DELETE /api/transactions/<id>
    Body: {user_id}
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Body debe ser JSON'}), 400
        
        # Validar entrada
        trans_id = validate_transaction_id(trans_id)
        user_id = validate_user_id(data.get('user_id'))
        
        # Eliminar
        success = Transaction.delete(trans_id, user_id)
        
        if not success:
            return jsonify({'error': 'Transacción no encontrada o acceso denegado'}), 404
        
        return jsonify({'message': 'Transacción eliminada'}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al eliminar transacción: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/transactions', methods=['GET', 'OPTIONS'])
def get_transactions():
    """
    Obtiene transacciones del usuario
    GET /api/transactions?user_id=<id>
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        user_id_str = request.args.get('user_id', '')
        user_id = validate_user_id(user_id_str)
        
        transactions = Transaction.get_all(user_id)
        
        return jsonify(transactions), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al obtener transacciones: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ============ RUTAS DE ESTADÍSTICAS ============

@app.route('/api/stats', methods=['GET', 'OPTIONS'])
def get_stats():
    """
    Obtiene estadísticas del usuario
    GET /api/stats?user_id=<id>
    """
    if request.method == 'OPTIONS':
        return '', 204
    
    try:
        user_id_str = request.args.get('user_id', '')
        user_id = validate_user_id(user_id_str)
        
        stats = Transaction.get_stats(user_id)
        
        return jsonify(stats), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

# ============ ERROR HANDLING ============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Método HTTP no permitido'}), 405

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Error interno: {str(error)}")
    return jsonify({'error': 'Error interno del servidor'}), 500

if __name__ == '__main__':
    app.run(debug=False, port=5001, host='127.0.0.1')
