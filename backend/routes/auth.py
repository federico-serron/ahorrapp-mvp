"""Rutas de autenticación"""
from flask import Blueprint, request, jsonify
import sqlite3
from utils.validators import ValidationError, validate_username, validate_password
from utils.security import hash_password, verify_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra nuevo usuario"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        username = validate_username(data.get('username', ''))
        password = validate_password(data.get('password', ''))
        
        # Hash password con salt
        password_hash, salt = hash_password(password)
        
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)',
                  (username, password_hash, salt))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        
        return jsonify({'id': user_id, 'username': username}), 201
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except sqlite3.IntegrityError:
        return jsonify({'error': 'Usuario ya existe'}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login de usuario"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        username = validate_username(data.get('username', ''))
        password = data.get('password', '')
        
        conn = sqlite3.connect('expenses.db')
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
        return jsonify({'error': 'Error interno'}), 500
