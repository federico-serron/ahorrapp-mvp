#!/bin/bash

# Script para iniciar Expense Tracker
# Carga variables de entorno desde .env

set -e

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Cargar .env
if [ -f .env ]; then
    echo -e "${GREEN}Cargando .env${NC}"
    export $(cat .env | grep -v '#' | xargs)
else
    echo -e "${RED}ERROR: archivo .env no encontrado${NC}"
    echo "Copia .env.example a .env y configura tu API key"
    exit 1
fi

# Validar API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "${RED}ERROR: ANTHROPIC_API_KEY no está configurada en .env${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Variables de entorno cargadas${NC}"
echo ""

# Detener servidores anteriores
echo "Deteniendo servidores previos..."
fuser -k 5001/tcp 3000/tcp 2>/dev/null || true
echo ""

# Detener servidores anteriores
echo "Deteniendo servidores previos..."
fuser -k 5001/tcp 3000/tcp 2>/dev/null || true
sleep 2

# Iniciar Backend
echo -e "${YELLOW}Iniciando Backend...${NC}"
cd backend
export FLASK_ENV=${FLASK_ENV:-development}
export PYTHONUNBUFFERED=1
python3 app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo -e "${GREEN}Backend iniciado (PID: $BACKEND_PID)${NC}"
sleep 3

# Validar Backend
if ! curl -s http://localhost:5001/api/stats?user_id=1 > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Backend no responde${NC}"
    tail -20 /tmp/backend.log
    exit 1
fi

cd ..

# Iniciar Frontend
echo -e "${YELLOW}Iniciando Frontend...${NC}"
cd frontend
python3 server.py > /tmp/frontend.log 2>&1 &
FRONTEND_PID=$!
echo -e "${GREEN}Frontend iniciado (PID: $FRONTEND_PID)${NC}"
sleep 2

# Validar Frontend
if ! curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "${RED}ERROR: Frontend no responde${NC}"
    tail -20 /tmp/frontend.log
    exit 1
fi

cd ..

echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ APLICACIÓN LISTA${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${GREEN}🌐 Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}⚙️  Backend:${NC}  http://localhost:5001"
echo ""
echo -e "${GREEN}📝 Credenciales:${NC}"
echo "   Usuario: test"
echo "   Password: test1234"
echo ""
echo -e "${GREEN}📝 O registrate creando una nueva cuenta${NC}"
echo ""
echo -e "${YELLOW}Logs:${NC}"
echo "   Backend:  tail -f /tmp/backend.log"
echo "   Frontend: tail -f /tmp/frontend.log"
echo ""
echo -e "${YELLOW}Detener servidores:${NC}"
echo "   kill $BACKEND_PID $FRONTEND_PID"
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════════════${NC}"

# Mantener script corriendo
wait
