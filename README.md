# 💰 Expense Tracker Pro - MVP

Sistema de gestión de gastos e ingresos con categorización automática, autenticación segura y gráficas interactivas.

## 🎯 Features

✅ **Autenticación Segura**
- Registro/Login con hashing PBKDF2
- Protección contra timing attacks
- Validación de inputs

✅ **Detección Inteligente**
- Categorización automática de transacciones
- Diferencia entre ingresos y gastos
- Análisis por palabras clave

✅ **Gestión Completa**
- Crear, editar, eliminar transacciones
- Historial completo
- Estadísticas en tiempo real

✅ **Seguridad**
- Sanitización XSS en frontend
- Validación en backend
- CORS configurado
- Headers de seguridad
- SQL Injection prevention con prepared statements

✅ **Interfaz**
- Dashboard moderno
- Gráficas interactivas (Chart.js)
- Responsive design
- Dark gradient theme

## 🏗️ Estructura del Proyecto

```
expense-tracker/
├── backend/
│   ├── app.py                 # Backend principal (Flask)
│   ├── wsgi.py               # Entry point para deployment
│   ├── expenses.db           # Base de datos SQLite
│   └── utils/                # Módulos de utilidad
│       ├── validators.py     # Validaciones
│       ├── security.py       # Hashing y tokens
│       └── categorizer.py    # Categorización
├── frontend/
│   ├── index.html            # Aplicación single-page
│   ├── server.py             # Servidor HTTP simple
│   └── public/
│       └── styles.css        # Estilos
├── requirements.txt          # Dependencias Python
├── Dockerfile                # Configuración Docker
├── Procfile                  # Para Heroku
├── railway.json              # Configuración Railway
└── README.md                 # Este archivo
```

## 🔒 Seguridad Implementada

### Backend
- **SQL Injection:** Prepared statements + validación de inputs
- **XSS:** Sanitización de strings, eliminación de caracteres de control
- **CSRF:** Validación en headers
- **Passwords:** PBKDF2 con 100k iteraciones + salt único
- **Timing Attacks:** constant-time comparison (hmac.compare_digest)
- **Validaciones:** Tipo, longitud, formato, rango
- **CORS:** Whitelist de orígenes permitidos
- **Headers:** X-Content-Type-Options, X-Frame-Options, X-XSS-Protection, HSTS

### Frontend
- **XSS:** Escaping de HTML (escapeHtml)
- **Validaciones:** HTML5 + JavaScript
- **Inputs:** minlength, maxlength, pattern, required
- **Content Security:** Sin eval, sin inline scripts riesgosos

## 📝 API Endpoints

### Autenticación
```
POST /api/auth/register
POST /api/auth/login
```

### Transacciones
```
GET  /api/transactions?user_id=1
POST /api/transactions
PUT  /api/transactions/<id>
DELETE /api/transactions/<id>
GET  /api/stats?user_id=1
```

## 🚀 Deployment

### Opción 1: Railway.app (Recomendado para MVP)

1. Haz fork/clone del repositorio
2. Conecta tu GitHub con Railway.app
3. Railway auto-detectará el Dockerfile
4. Configura variables de entorno:
   ```
   FLASK_ENV=production
   ANTHROPIC_API_KEY=tu_key
   PORT=8000
   ```
5. Deploy automático en cada push

### Opción 2: Local (Desarrollo)

**Backend:**
```bash
cd backend
pip install -r ../requirements.txt
export ANTHROPIC_API_KEY="tu_key"
python app.py
```

**Frontend:**
```bash
cd frontend
python server.py
```

Abre: http://localhost:3000

## 🔑 Variables de Entorno

```bash
FLASK_ENV=production          # production o development
PORT=8000                     # Puerto (Railway asigna automático)
ANTHROPIC_API_KEY=sk-...     # Tu API key de Anthropic
```

## 📊 Base de Datos

SQLite local (expenses.db) con 2 tablas:

**users**
- id (PK)
- username (UNIQUE)
- password_hash
- password_salt
- created_at

**transactions**
- id (PK)
- user_id (FK)
- description
- amount
- category
- type (income/expense)
- created_at

## 🎨 Tecnologías

**Backend:**
- Flask 2.3.3
- SQLite3
- Python 3.12
- PBKDF2 (hashlib)

**Frontend:**
- HTML5
- Vanilla JavaScript
- Chart.js 4.4.0
- CSS3 (Gradient, Grid, Flexbox)

## 📖 Documentación de Código

### Backend

**app.py** - Aplicación principal
- Validaciones sanitización
- Rutas de autenticación
- Rutas de transacciones
- Configuración de seguridad

**Flujo de Validación:**
```
Input → Validar tipo → Sanitizar → Validar longitud/formato 
→ Validar rango → DB (prepared statements) → Response
```

### Frontend

**index.html** - SPA completa
- Estado centralizado (State object)
- Escaping XSS (escapeHtml)
- Validaciones antes de submit
- Chart.js para gráficas
- Modal para edición

**Flujo de Seguridad:**
```
User Input → HTML5 validation → JS validation 
→ Escape HTML → Fetch API → Backend validation → DB
```

## 🧪 Testing Manual

1. **Registro:** Crea usuario `test` / `test1234`
2. **Login:** Inicia sesión
3. **Ingreso:** Descripción "Sueldo mensual", Monto: 2000
   - Debe detectar como INCOME automáticamente
4. **Gasto:** Descripción "Cine con amigos", Monto: 20
   - Debe categorizar como Entretenimiento
5. **Editar:** Click en "Editar", modifica y guarda
6. **Eliminar:** Click en "Editar" → "Eliminar"
7. **Gráficas:** Deberían actualizarse en tiempo real

## 🐛 Troubleshooting

**"Error de conexión"**
- Verifica que backend corra en puerto 5001 (local) o URL correcta (prod)
- Revisa CORS en backend

**"Usuario ya existe"**
- El username es único por diseño
- Usa otro nombre

**"Monto excede límite"**
- Máximo $1,000,000 por transacción
- Diseñado para evitar abusos

## 📝 Próximos Pasos

- [ ] Autenticación con JWT tokens
- [ ] 2FA (Two-Factor Authentication)
- [ ] Exportar a CSV/PDF
- [ ] Presupuestos mensuales
- [ ] Notificaciones
- [ ] App móvil
- [ ] Sincronización en la nube

## 👤 Autor

Molty - Asistente Virtual de OpenClaw

## 📄 Licencia

MIT - Úsalo como quieras

---

**¿Preguntas? Problemas?**
Revisa la sección de Seguridad implementada para entender las protecciones.
