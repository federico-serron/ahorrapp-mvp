"""Rutas de transacciones"""
from flask import Blueprint, request, jsonify
import sqlite3
from datetime import datetime
from utils.validators import ValidationError, validate_description, validate_amount, validate_user_id
from utils.categorizer import categorize_transaction

trans_bp = Blueprint('transactions', __name__)

@trans_bp.route('', methods=['POST'])
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
        
        conn = sqlite3.connect('expenses.db')
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
        return jsonify({'error': 'Error interno'}), 500

@trans_bp.route('/<int:trans_id>', methods=['PUT'])
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
        
        conn = sqlite3.connect('expenses.db')
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
        return jsonify({'error': 'Error interno'}), 500

@trans_bp.route('/<int:trans_id>', methods=['DELETE'])
def delete_transaction(trans_id):
    """Elimina transacción"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Datos inválidos'}), 400
        
        user_id = validate_user_id(data.get('user_id'))
        
        conn = sqlite3.connect('expenses.db')
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id=? AND user_id=?', (trans_id, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({'message': 'Eliminado'}), 200
    
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Error interno'}), 500

@trans_bp.route('', methods=['GET'])
def get_transactions():
    """Obtiene transacciones del usuario"""
    try:
        user_id = validate_user_id(request.args.get('user_id'))
        
        conn = sqlite3.connect('expenses.db')
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
        return jsonify({'error': 'Error interno'}), 500

@trans_bp.route('/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del usuario"""
    try:
        user_id = validate_user_id(request.args.get('user_id'))
        
        conn = sqlite3.connect('expenses.db')
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
        return jsonify({'error': 'Error interno'}), 500
