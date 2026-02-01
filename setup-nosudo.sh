#!/bin/bash

echo "🚀 Instalando Expense Tracker (sin sudo)..."

# Create virtual environment
echo "🐍 Creando Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Install Python packages
echo "📦 Instalando dependencias Python..."
pip install --upgrade pip
pip install -r ../requirements.txt

deactivate
cd ..

# Setup .env
echo "⚙️  Configurando .env..."
cp .env.example .env
echo ""
echo "⚠️  IMPORTANTE: Edita .env con tu ANTHROPIC_API_KEY"
cat .env

# Setup React
echo ""
echo "⚛️  Configurando frontend React..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup completado!"
echo ""
echo "📝 Para ejecutar:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd /home/pepe/expense-tracker/backend"
echo "  source venv/bin/activate"
echo "  python3 app.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd /home/pepe/expense-tracker/frontend"
echo "  npm start"
echo ""
echo "🌐 Abre http://localhost:3000"
