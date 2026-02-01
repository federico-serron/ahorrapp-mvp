import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [expenses, setExpenses] = useState([]);
  const [stats, setStats] = useState(null);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch expenses on mount
  useEffect(() => {
    fetchExpenses();
    fetchStats();
  }, []);

  const fetchExpenses = async () => {
    try {
      const response = await axios.get('/api/expenses');
      setExpenses(response.data);
    } catch (error) {
      console.error('Error fetching expenses:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('/api/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!description.trim() || !amount) {
      setMessage('Por favor completa todos los campos');
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      await axios.post('/api/expenses', {
        description,
        amount: parseFloat(amount)
      });

      setMessage('✅ Gasto registrado correctamente!');
      setDescription('');
      setAmount('');
      
      // Refresh data
      await fetchExpenses();
      await fetchStats();

      // Clear message after 3 seconds
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('❌ Error al registrar el gasto');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        <h1>💰 Expense Tracker</h1>
        <p>Registra tus gastos y déjate categorizar por IA</p>
      </div>

      {/* Form */}
      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Descripción del gasto</label>
            <input
              type="text"
              placeholder="Ej: Almuerzo en restaurant"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label>Monto (en tu moneda)</label>
            <input
              type="number"
              placeholder="Ej: 25.50"
              step="0.01"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              disabled={loading}
            />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Registrando...' : 'Registrar Gasto'}
          </button>
        </form>

        {message && (
          <div className={message.includes('✅') ? 'success-message' : 'error-message'} 
               style={{marginTop: '15px'}}>
            {message}
          </div>
        )}
      </div>

      {/* Stats */}
      {stats && (
        <div className="card">
          <h2>Estadísticas</h2>
          <div className="stats">
            <div className="stat-card">
              <div className="stat-value">${stats.total.toFixed(2)}</div>
              <div className="stat-label">Total Gastado</div>
            </div>
            <div className="stat-card">
              <div className="stat-value">{stats.count}</div>
              <div className="stat-label">Total Transacciones</div>
            </div>
          </div>
        </div>
      )}

      {/* Expenses List */}
      <div className="card">
        <h2>Historial de Gastos</h2>
        {expenses.length === 0 ? (
          <div className="no-expenses">No hay gastos registrados aún</div>
        ) : (
          <div className="expenses-list">
            {expenses.map((expense) => (
              <div key={expense.id} className="expense-item">
                <div className="expense-header">
                  <div>
                    <strong>{expense.description}</strong>
                  </div>
                  <div className="expense-amount">${expense.amount.toFixed(2)}</div>
                </div>
                <div>
                  <span className="expense-category">{expense.category}</span>
                  <span className={`expense-sentiment ${expense.sentiment}`}>
                    {expense.sentiment === 'positive' ? '✅ Necesario' : '⚠️ Discretional'}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
