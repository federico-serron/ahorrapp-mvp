"""
Módulo de modelos de base de datos
"""
import sqlite3
from datetime import datetime
from typing import List, Optional, Dict, Any
from utils.security import hash_password, verify_password

DATABASE = 'expenses.db'

def init_db():
    """
    Inicializa la base de datos con tablas
    """
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Tabla de usuarios (mejorada con salt)
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE NOT NULL,
                  password_hash TEXT NOT NULL,
                  password_salt TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # Tabla de transacciones
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER NOT NULL,
                  description TEXT NOT NULL,
                  amount REAL NOT NULL,
                  category TEXT,
                  type TEXT DEFAULT 'expense',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    conn.commit()
    conn.close()

class User:
    """Modelo de usuario"""
    
    @staticmethod
    def create(username: str, password: str) -> Optional[int]:
        """Crea nuevo usuario"""
        password_hash, salt = hash_password(password)
        
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        try:
            c.execute('INSERT INTO users (username, password_hash, password_salt) VALUES (?, ?, ?)',
                      (username, password_hash, salt))
            conn.commit()
            user_id = c.lastrowid
            conn.close()
            return user_id
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def authenticate(username: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica usuario"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT id, password_hash, password_salt FROM users WHERE username = ?', (username,))
        result = c.fetchone()
        conn.close()
        
        if not result:
            return None
        
        user_id, stored_hash, salt = result
        
        if verify_password(password, stored_hash, salt):
            return {'id': user_id, 'username': username}
        
        return None

class Transaction:
    """Modelo de transacción"""
    
    @staticmethod
    def create(user_id: int, description: str, amount: float, category: str, trans_type: str) -> Optional[int]:
        """Crea nueva transacción"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        now = datetime.now().isoformat()
        c.execute('''INSERT INTO transactions 
                     (user_id, description, amount, category, type, created_at) 
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (user_id, description, amount, category, trans_type, now))
        conn.commit()
        trans_id = c.lastrowid
        conn.close()
        
        return trans_id
    
    @staticmethod
    def get_all(user_id: int) -> List[Dict[str, Any]]:
        """Obtiene todas las transacciones del usuario"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''SELECT id, description, amount, category, type, created_at 
                     FROM transactions 
                     WHERE user_id=? 
                     ORDER BY created_at DESC''',
                  (user_id,))
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
        return transactions
    
    @staticmethod
    def update(trans_id: int, user_id: int, description: str, amount: float, category: str, trans_type: str) -> bool:
        """Actualiza transacción"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''UPDATE transactions 
                     SET description=?, amount=?, category=?, type=? 
                     WHERE id=? AND user_id=?''',
                  (description, amount, category, trans_type, trans_id, user_id))
        conn.commit()
        success = c.rowcount > 0
        conn.close()
        return success
    
    @staticmethod
    def delete(trans_id: int, user_id: int) -> bool:
        """Elimina transacción"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('DELETE FROM transactions WHERE id=? AND user_id=?', (trans_id, user_id))
        conn.commit()
        success = c.rowcount > 0
        conn.close()
        return success
    
    @staticmethod
    def get_stats(user_id: int) -> Dict[str, Any]:
        """Obtiene estadísticas del usuario"""
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        
        # Total gastos
        c.execute('SELECT SUM(amount) FROM transactions WHERE user_id=? AND type="expense"', (user_id,))
        total_expenses = c.fetchone()[0] or 0
        
        # Total ingresos
        c.execute('SELECT SUM(amount) FROM transactions WHERE user_id=? AND type="income"', (user_id,))
        total_income = c.fetchone()[0] or 0
        
        # Por categoría
        c.execute('''SELECT category, COUNT(*), SUM(amount) 
                     FROM transactions 
                     WHERE user_id=? AND type="expense" 
                     GROUP BY category''', (user_id,))
        by_category = [{'category': row[0], 'count': row[1], 'total': row[2]} for row in c.fetchall()]
        
        conn.close()
        
        return {
            'total_expenses': total_expenses,
            'total_income': total_income,
            'balance': total_income - total_expenses,
            'by_category': by_category
        }
