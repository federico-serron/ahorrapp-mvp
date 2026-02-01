# 📁 Estructura de Expense Tracker

Explicación modular y legible de cómo está organizada la aplicación.

---

## 🏠 Estructura General

```
expense-tracker/
├── backend/                  # Servidor Flask (API)
│   ├── app.py               # Archivo principal (PUNTO DE ENTRADA)
│   ├── app_old.py           # Backup de versión anterior
│   ├── app_secure.py        # Nueva versión segura
│   ├── db/
│   │   └── models.py        # Modelos de base de datos
│   └── utils/
│       ├── validators.py    # Validación de entrada
│       ├── security.py      # Hashing y tokens
│       └── categorizer.py   # Categorización automática
│
├── frontend/                # Cliente web (React/Vanilla JS)
│   ├── index.html           # HTML principal (PUNTO DE ENTRADA)
│   ├── server.py            # Servidor simple Python
│   ├── css/
│   │   └── styles.css       # Estilos CSS (modular)
│   └── js/
│       ├── security.js      # Sanitización XSS
│       ├── api.js           # Llamadas HTTP a backend
│       ├── ui.js            # Manejo de interfaz
│       └── app.js           # Lógica principal
│
├── SECURITY.md              # Documentación de seguridad
├── ESTRUCTURA.md            # Este archivo
├── QUICKSTART.md            # Guía rápida
└── README.md                # Documentación general
```

---

## 🔧 BACKEND - Estructura Modular

### `backend/app.py` - Punto de Entrada

Archivo principal que:
- Configura Flask
- Define rutas API
- Maneja errores
- Agregaheaders de seguridad

**Rutas principales:**
```
POST   /api/auth/register      # Crear usuario
POST   /api/auth/login         # Iniciar sesión
POST   /api/transactions       # Crear transacción
PUT    /api/transactions/<id>  # Actualizar transacción
DELETE /api/transactions/<id>  # Eliminar transacción
GET    /api/transactions       # Listar transacciones
GET    /api/stats              # Obtener estadísticas
```

### `backend/db/models.py` - Modelos de Datos

Define cómo interactuar con la base de datos:

**Clase User:**
```python
User.create(username, password)        # Crear usuario
User.authenticate(username, password)  # Login
```

**Clase Transaction:**
```python
Transaction.create(user_id, ...)       # Crear transacción
Transaction.get_all(user_id)           # Listar todas
Transaction.update(trans_id, ...)      # Actualizar
Transaction.delete(trans_id, ...)      # Eliminar
Transaction.get_stats(user_id)         # Estadísticas
```

**Función init_db():**
- Crea tablas si no existen
- Schema:
  - `users`: id, username, password_hash, password_salt, created_at
  - `transactions`: id, user_id, description, amount, category, type, created_at

### `backend/utils/validators.py` - Validación

Valida y sanitiza TODAS las entradas:

```python
validate_username(username)      # 3-20 chars, alfanumérico
validate_password(password)      # Mínimo 4 chars
validate_description(desc)       # Máximo 500 chars
validate_amount(amount)          # Número, no cero, máx $1M
validate_user_id(user_id)        # Integer > 0
```

**Uso:**
```python
from utils.validators import validate_username, ValidationError

try:
    username = validate_username(user_input)
except ValidationError as e:
    return jsonify({'error': str(e)}), 400
```

### `backend/utils/security.py` - Seguridad

Funciones de criptografía:

```python
hash_password(password, salt=None)     # PBKDF2 con salt
verify_password(password, hash, salt)  # Verifica contraseña
generate_token(length=32)              # Token aleatorio seguro
```

**Protecciones:**
- PBKDF2-HMAC-SHA256
- 100,000 iteraciones
- Constant-time comparison (timing attack safe)

### `backend/utils/categorizer.py` - Categorización

Detecta automáticamente:
- **Tipo**: income vs expense
- **Categoría**: Alimentacion, Transporte, etc.

```python
category, trans_type = categorize_transaction("Sueldo mensual")
# Retorna: ('Ingresos', 'income')

category, trans_type = categorize_transaction("Cine")
# Retorna: ('Entretenimiento', 'expense')
```

---

## 💻 FRONTEND - Estructura Modular

### `frontend/index.html` - Punto de Entrada

HTML principal que:
- Carga scripts en orden correcto
- Define estructura DOM
- Attributes de seguridad (maxlength, max, step)

**Orden de carga (IMPORTANTE):**
1. `security.js` - Funciones base
2. `api.js` - Llamadas API
3. `ui.js` - Manejo UI
4. `app.js` - Lógica (ejecuta último)

### `frontend/js/security.js` - Sanitización

Previene XSS y valida entrada:

```javascript
escapeHtml(text)                 # Escapa <, >, &, ", '
sanitizeInput(value, maxLen)     # Limpia strings
validateUsername(username)       # Valida formato
validatePassword(password)       # Valida contraseña
validateDescription(desc)        # Valida descripción
validateAmount(amount)           # Valida número
SecureStorage.set/get/remove()   # localStorage seguro
```

**Uso:**
```javascript
const validation = validateFormData(data, [
    { name: 'username', type: 'username' },
    { name: 'password', type: 'password' }
]);

if (!validation.valid) {
    // Mostrar error
}
```

### `frontend/js/api.js` - Llamadas HTTP

Encapsula TODAS las llamadas a API:

```javascript
API.auth.register(username, password)
API.auth.login(username, password)
API.transactions.create(userId, desc, amount)
API.transactions.getAll(userId)
API.transactions.update(id, userId, desc, amount)
API.transactions.delete(id, userId)
API.stats.get(userId)
```

**Ventaja:**
- URL centralizada
- Error handling consistente
- Fácil de cambiar a producción

### `frontend/js/ui.js` - Interfaz de Usuario

Maneja TODO lo visual:

```javascript
UI.showAuthSection()                           # Muestra login
UI.showAppSection(username)                    # Muestra app
UI.switchTab(tab)                              # Cambia tabs
UI.showMessage(id, msg, type)                  # Muestra msg
UI.renderTransactions(transactions)            # Lista transacciones
UI.updateStats(stats)                          # Actualiza números
UI.openEditModal(id, desc, amount)             # Abre modal
UI.closeEditModal()                            # Cierra modal
```

**Patrón:**
- Todos los renders usan `escapeHtml()`
- Todos los updates pasan por función UI
- Fácil de testear y modificar

### `frontend/js/app.js` - Lógica Principal

Orquesta el flujo de la aplicación:

```javascript
initApp()                      # Init cuando carga DOM
handleLogin()                  # Login form submit
handleRegister()               # Register form submit
handleAddTransaction()         # Nueva transacción
handleEditTransaction()        # Editar transacción
loadAppData()                  # Fetch data del servidor
updateCharts(stats)            # Actualiza gráficas
```

**Patrón de flujo:**
1. User acción (click, submit)
2. Validar entrada → `validateFormData()`
3. Llamar API → `API.transactions.create()`
4. Actualizar UI → `UI.renderTransactions()`
5. Mostrar mensaje → `UI.showMessage()`

### `frontend/css/styles.css` - Estilos

Organizado por secciones para legibilidad:

```
/* ============ BASE ============ */
/* ============ HEADER ============ */
/* ============ FORMS ============ */
/* ============ BUTTONS ============ */
/* ============ STATS ============ */
/* ============ CHARTS ============ */
/* ============ TRANSACCIONES ============ */
/* ============ MODAL ============ */
/* ============ RESPONSIVE ============ */
```

Cada sección es un bloque independiente y fácil de encontrar.

---

## 🔄 Flujo de Datos

### Registro:

```
Usuario escribe username/password
  ↓
Frontend valida (security.js)
  ↓
API.auth.register() envía a backend
  ↓
Backend valida (validators.py)
  ↓
Backend hashea contraseña (security.py)
  ↓
Backend guarda en DB (models.py)
  ↓
Retorna success o error
  ↓
UI actualiza (ui.js)
```

### Crear Transacción:

```
Usuario ingresa descripción/monto
  ↓
Frontend valida (security.js)
  ↓
API.transactions.create() envía
  ↓
Backend valida (validators.py)
  ↓
Backend categoriza (categorizer.py)
  ↓
Backend guarda en DB (models.py)
  ↓
Frontend fetch actualiza lista
  ↓
UI.renderTransactions() muestra
  ↓
updateCharts() actualiza gráficas
```

---

## 🛠️ Cómo Agregar Funcionalidad

### Agregar Nuevo Campo en Transacción

**1. Backend - DB Schema** (`backend/db/models.py`):
```python
# En init_db(), agregar columna:
c.execute('ALTER TABLE transactions ADD COLUMN new_field TEXT')
```

**2. Backend - Validador** (`backend/utils/validators.py`):
```python
def validate_new_field(value: str) -> str:
    # Tu lógica...
    return value
```

**3. Backend - Ruta** (`backend/app.py`):
```python
@app.route('/api/transactions', methods=['POST'])
def add_transaction():
    # ...
    new_field = validate_new_field(data.get('new_field'))
    # ...
```

**4. Frontend - Validador** (`frontend/js/security.js`):
```javascript
function validateNewField(field) {
    // Tu lógica...
    return { valid: true/false, error: '...' };
}
```

**5. Frontend - HTML** (`frontend/index.html`):
```html
<input id="newField" maxlength="X" required>
```

**6. Frontend - Formulario** (`frontend/js/app.js`):
```javascript
const newField = document.getElementById('newField').value;
const validation = validateNewField(newField);
```

---

## 📊 Ejemplo: Editar Transacción

### Frontend (ui.js + app.js):
```
User Click Editar
  ↓ UI.openEditModal(id, desc, amount)
  ↓ Modal aparece con valores
  ↓ User cambia valores
  ↓ Form submit
  ↓ handleEditTransaction()
  ↓ Validar (validateFormData)
  ↓ API.transactions.update()
```

### Backend (app.py):
```
PUT /api/transactions/<id>
  ↓ Obtener JSON
  ↓ Validar entrada (validators.py)
  ↓ Verificar que sea usuario propietario
  ↓ Transaction.update() en DB
  ↓ Retornar 200 OK
```

### Frontend (continuación):
```
API retorna success
  ↓ loadAppData() (fetch updated)
  ↓ UI.renderTransactions() (redraw list)
  ↓ updateCharts() (redraw graphs)
  ↓ UI.closeEditModal()
```

---

## 🧪 Testing Manual

### Probar Validación XSS:
```
Descripción: <script>alert('xss')</script>
  ✅ Frontend escapa antes de enviar
  ✅ Backend no acepta caracteres de control
  ✅ En lista aparece como texto
```

### Probar SQL Injection:
```
Username: ' OR '1'='1
  ✅ Frontend rechaza (no alfanumérico)
  ✅ Backend valida regex
```

### Probar Límites:
```
Monto: 999999999
  ✅ Frontend rechaza (max 1000000)
  ✅ Backend rechaza si pasa
```

---

## 🚀 Próximas Mejoras

- [ ] Autenticación con tokens JWT
- [ ] Rate limiting en API
- [ ] CSRF protection
- [ ] Two-factor authentication
- [ ] Exportar a CSV/PDF
- [ ] Filtro por rango de fechas
- [ ] Búsqueda de transacciones
- [ ] Temas oscuro/claro
- [ ] Aplicación móvil

---

**Objetivo:** Código limpio, modular y seguro que cualquiera pueda entender y modificar.

**Última actualización:** 2026-02-01
