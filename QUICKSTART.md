# 🚀 QUICKSTART - Expense Tracker

## ⚡ Paso 1: Instalar dependencias (UNA SOLA VEZ)

Abre una terminal y ejecuta:

```bash
cd /home/pepe/expense-tracker
bash setup-nosudo.sh
```

Esto va a:
- Crear un virtual environment Python
- Instalar todas las dependencias
- Instalar dependencias React

## 🔑 Paso 2: Configurar tu API Key

Abre `/home/pepe/expense-tracker/.env` y reemplaza:

```
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

Por tu API key de Anthropic (puedes obtenerla en https://console.anthropic.com/)

## 🎯 Paso 3: Ejecutar la app

### Opción A: Ejecutar ambos servidores automáticamente

```bash
cd /home/pepe/expense-tracker
bash run.sh
```

Esto inicia:
- Backend Flask en http://localhost:5001
- Frontend React en http://localhost:3000

### Opción B: Ejecutar en terminales separadas (más control)

**Terminal 1 - Backend:**
```bash
cd /home/pepe/expense-tracker/backend
source venv/bin/activate
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd /home/pepe/expense-tracker/frontend
npm start
```

## 🌐 Acceder a la app

Abre tu navegador en: **http://localhost:3000**

## ✨ Features

1. **Registrar Gasto**: Ingresa descripción y monto
2. **IA Automática**: Claude categoriza y evalúa el gasto
3. **Categorías**: Alimentación, Transporte, Entretenimiento, Servicios, Salud, Compras, Otros
4. **Sentimiento**: Gasto Necesario (verde) vs Discretional (rojo)
5. **Google Sheets**: Todos los gastos se sincronizan (opcional, ver abajo)
6. **Estadísticas**: Total gastado y cantidad de transacciones

## 🔌 Google Sheets Integration (Opcional)

Para guardar en Google Sheets:

1. Crea un Google Sheet
2. Obtén el ID de la hoja (está en la URL)
3. Descarga credentials.json de Google Cloud Console
4. Coloca credentials.json en `/home/pepe/expense-tracker/backend/`
5. Edita `.env` y configura `GOOGLE_SHEET_ID`

## 🛠️ Troubleshooting

**"Module not found: anthropic"**
```bash
cd backend && source venv/bin/activate && pip install anthropic
```

**"npm: command not found"**
```bash
Node.js está instalado, pero npm no está en PATH. Reinicia la terminal.
```

**Backend da error en puerto 5001**
```bash
lsof -i :5001  # Ver qué ocupa el puerto
kill -9 <PID>  # Matar el proceso
```

## 📝 Archivo de estructura

```
/home/pepe/expense-tracker/
├── backend/
│   ├── app.py              # API Flask
│   ├── venv/               # Virtual environment Python
│   └── expenses.db         # Base de datos SQLite
├── frontend/
│   ├── public/             # HTML + CSS
│   ├── src/                # React components
│   └── node_modules/       # Dependencias Node
├── .env                    # Variables de entorno
├── requirements.txt        # Dependencias Python
├── setup-nosudo.sh         # Script de instalación
├── run.sh                  # Script para ejecutar todo
└── README.md               # Documentación completa
```

## 🎉 ¡Listo!

Disfruta tu Expense Tracker. 💰✨
