#!/bin/bash

PROJECT_DIR=$(cd "$(dirname "$0")" && pwd)

echo "🚀 Expense Tracker - Iniciando..."
echo "📁 Proyecto: $PROJECT_DIR"
echo ""

# Check if backend venv exists
if [ ! -d "$PROJECT_DIR/backend/venv" ]; then
    echo "⚠️  Entorno virtual no encontrado. Ejecuta primero:"
    echo "   bash setup-nosudo.sh"
    exit 1
fi

# Check if .env is configured
if grep -q "your_anthropic_api_key_here" "$PROJECT_DIR/.env"; then
    echo "⚠️  .env no está configurado!"
    echo "   Edita .env y configura tu ANTHROPIC_API_KEY"
    exit 1
fi

# Start backend in background
echo "🐍 Iniciando backend (puerto 5001)..."
cd "$PROJECT_DIR/backend"
source venv/bin/activate
python3 app.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait a bit for backend to start
sleep 2

# Start frontend
echo ""
echo "⚛️  Iniciando frontend (puerto 3000)..."
cd "$PROJECT_DIR/frontend"
npm start

# Cleanup
trap "kill $BACKEND_PID 2>/dev/null" EXIT
