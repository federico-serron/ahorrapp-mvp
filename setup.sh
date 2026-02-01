#!/bin/bash

echo "🚀 Instalando Expense Tracker..."

# Install system dependencies
echo "📦 Instalando dependencias del sistema..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Create .env file
echo "⚙️  Configurando .env..."
cat > .env << EOF
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-sk-}
GOOGLE_SHEET_ID=${GOOGLE_SHEET_ID:-}
FLASK_ENV=development
EOF

# Setup Python backend
echo "🐍 Configurando backend Python..."
cd backend
pip3 install -r ../requirements.txt
cd ..

# Setup React frontend
echo "⚛️  Configurando frontend React..."
cd frontend
npm install
cd ..

echo "✅ Setup completado!"
echo ""
echo "📝 Próximos pasos:"
echo "1. Edita .env con tu ANTHROPIC_API_KEY"
echo "2. Terminal 1: cd backend && python3 app.py"
echo "3. Terminal 2: cd frontend && npm start"
echo ""
echo "🌐 Abre http://localhost:3000 en tu navegador"
