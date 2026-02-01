"""
Módulo de base de datos - Operaciones CRUD
"""
import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime

DATABASE = 'expenses.db'

def get_connection():
    """Obtiene conexión a BD"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa tablas"""
    conn = get_connection()
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  password_salt TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER NOT NULL,
                  description TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT,
                  type TEXT DEFAULT 'expense',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  updated_at TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE)''')
    
    # Crear índices para mejor performance
    c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_user ON transactions(user_id)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_transactions_type ON transactions(type)')
    
    conn.commit()
    conn.close()

# ==================== USERS ====================

def create_user(username: str, password_hash: str, password_salt: str) -> int:
    """Crea nuevo usuario"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute(
        'INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)',
        (username, password_hash, password_salt)
    )
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    
    return user_id

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Obtiene usuario por nombre de usuario"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT id, username, password_hash, password_salt FROM users WHERE username = ?',
              (username,))
    result = c.fetchone()
    conn.close()
    
    return dict(result) if result else None

def user_exists(username: str) -> bool:
    """Verifica si usuario existe"""
    return get_user_by_username(username) is not None

# ==================== TRANSACTIONS ====================

def create_transaction(user_id: int, description: str, amount: float,
                       category: str, trans_type: str) -> int:
    """Crea nueva transacción"""
    conn = get_connection()
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute(
        '''INSERT INTO transactions
           (user_id, description, amount, category, type, created_at)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (user_id, description, amount, category, trans_type, now)
    )
    conn.commit()
    trans_id = c.lastrowid
    conn.close()
    
    return trans_id

def get_transaction(trans_id: int, user_id: int) -> Optional[Dict[str, Any]]:
    """Obtiene transacción (verifica pertenencia a usuario)"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute(
        'SELECT * FROM transactions WHERE id = ? AND user_id = ?',
        (trans_id, user_id)
    )
    result = c.fetchone()
    conn.close()
    
    return dict(result) if result else None

def get_user_transactions(user_id: int, limit: int = 1000) -> List[Dict[str, Any]]:
    """Obtiene transacciones del usuario"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute(
        '''SELECT id, description, amount, category, type, created_at
           FROM transactions
           WHERE user_id = ?
           ORDER BY created_at DESC
           LIMIT ?''',
        (user_id, limit)
    )
    
    results = c.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

def update_transaction(trans_id: int, user_id: int, description: str,
                      amount: float, category: str, trans_type: str) -> bool:
    """Actualiza transacción (verifica pertenencia)"""
    conn = get_connection()
    c = conn.cursor()
    
    now = datetime.now().isoformat()
    c.execute(
        '''UPDATE transactions
           SET description = ?, amount = ?, category = ?, type = ?, updated_at = ?
           WHERE id = ? AND user_id = ?''',
        (description, amount, category, trans_type, now, trans_id, user_id)
    )
    
    conn.commit()
    success = c.rowcount > 0
    conn.close()
    
    return success

def delete_transaction(trans_id: int, user_id: int) -> bool:
    """Elimina transacción (verifica pertenencia)"""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('DELETE FROM transactions WHERE id = ? AND user_id = ?',
              (trans_id, user_id))
    
    conn.commit()
    success = c.rowcount > 0
    conn.close()
    
    return success

# ==================== STATS ====================

def get_user_stats(user_id: int) -> Dict[str, Any]:
    """Obtiene estadísticas del usuario"""
    conn = get_connection()
    c = conn.cursor()
    
    # Total ingresos
    c.execute(
        'SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = "income"',
        (user_id,)
    )
    total_income = c.fetchone()['total'] or 0
    
    # Total gastos
    c.execute(
        'SELECT SUM(amount) as total FROM transactions WHERE user_id = ? AND type = "expense"',
        (user_id,)
    )
    total_expenses = c.fetchone()['total'] or 0
    
    # Por categoría
    c.execute(
        '''SELECT category, COUNT(*) as count, SUM(amount) as total
           FROM transactions
           WHERE user_id = ? AND type = "expense"
           GROUP BY category''',
        (user_id,)
    )
    
    by_category = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'balance': total_income - total_expenses,
        'by_category': by_category
    }
