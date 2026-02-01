# 🔒 Seguridad de Expense Tracker

Esta aplicación ha sido refactorizada con múltiples capas de seguridad para proteger contra ataques comunes.

---

## 🛡️ Protecciones Implementadas

### Backend (Flask)

#### 1. **SQL Injection Prevention**
- ✅ Uso de parámetros preparados en ALL queries
- ✅ Nunca se concatenan strings directamente en SQL
- ✅ Validación de tipos en base de datos

```python
# ✅ SEGURO - Usa parámetros
c.execute('SELECT * FROM users WHERE username = ?', (username,))

# ❌ INSEGURO - NUNCA hacer esto
c.execute(f'SELECT * FROM users WHERE username = {username}')
```

#### 2. **Password Security**
- ✅ Hash PBKDF2 con 100,000 iteraciones
- ✅ Salt único para cada contraseña
- ✅ Constant-time comparison para evitar timing attacks
- ✅ Validation de mínimo 4, máximo 128 caracteres

```python
# En security.py
password_hash, salt = hash_password(password)
```

#### 3. **Input Validation & Sanitization**
- ✅ Validador personalizado para cada campo
- ✅ Límites de longitud
- ✅ Expresiones regulares para formato
- ✅ Sanitización de caracteres de control

```python
# En validators.py
def validate_username(username) -> str:
    # Valida: 3-20 chars, solo alfanuméricos
    if not re.match(r'^[a-z0-9_-]+$', username):
        raise ValidationError(...)
```

#### 4. **CORS Security**
- ✅ CORS restringido a localhost en desarrollo
- ✅ Métodos permitidos específicos
- ✅ Headers de seguridad

```python
CORS(app, 
     resources={r"/api/*": {
         "origins": ["http://localhost:3000"],
         "methods": ["GET", "POST", "PUT", "DELETE"]
     }})
```

#### 5. **Security Headers**
- ✅ X-Content-Type-Options: nosniff
- ✅ X-Frame-Options: DENY
- ✅ X-XSS-Protection: 1; mode=block
- ✅ Strict-Transport-Security
- ✅ Content-Security-Policy

#### 6. **Error Handling**
- ✅ No se exponen detalles internos en errores
- ✅ Logging de errores en servidor
- ✅ Mensajes genéricos al cliente

### Frontend (JavaScript/HTML)

#### 1. **XSS Prevention**
- ✅ Escapado de HTML en todos los renders
- ✅ Uso de `textContent` vs `innerHTML`
- ✅ Validación de entrada antes de renderizar

```javascript
// ✅ SEGURO - Escapa HTML
document.textContent = escapeHtml(userInput);

// ❌ INSEGURO
document.innerHTML = userInput;
```

#### 2. **Input Validation**
- ✅ Validación en cliente y servidor (double validation)
- ✅ Límites de longitud
- ✅ Expresiones regulares
- ✅ Tipos de datos verificados

```javascript
// En security.js
function validateUsername(username) {
    if (!/^[a-z0-9_-]+$/i.test(username)) {
        return { valid: false, error: 'Inválido' };
    }
}
```

#### 3. **Secure Storage**
- ✅ localStorage con wrapper seguro
- ✅ Solo datos no sensibles guardados
- ✅ Username escapado en storage

```javascript
// En security.js
SecureStorage.set('user', {
    id: value.id,
    username: escapeHtml(value.username),
    token: value.token
});
```

#### 4. **API Calls**
- ✅ HTTPS ready (headers de seguridad)
- ✅ Encapsulación en módulo API
- ✅ Error handling centralizado

```javascript
// En api.js
const response = await fetch(url, {
    method,
    headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
    }
});
```

#### 5. **Attribute Validation**
- ✅ maxlength en inputs HTML
- ✅ min/max en number inputs
- ✅ step en cantidad

```html
<input 
    type="number" 
    id="amount"
    step="0.01"
    max="1000000"
    required>
```

---

## 📁 Estructura Modular

### Backend

```
backend/
├── app.py                 # Aplicación principal (SEGURA)
├── app_old.py            # Versión anterior (backup)
├── app_secure.py         # Nueva versión segura
├── db/
│   └── models.py        # Modelos de DB (User, Transaction)
└── utils/
    ├── validators.py    # Validación e sanitización
    ├── security.py      # Hash, tokens, verificación
    └── categorizer.py   # Categorización automática
```

### Frontend

```
frontend/
├── index.html           # HTML principal
├── css/
│   └── styles.css      # Estilos (modular por sección)
└── js/
    ├── security.js     # Sanitización y validación
    ├── api.js          # Llamadas a API
    ├── ui.js           # Manejo de UI
    └── app.js          # Lógica principal
```

---

## 🔍 Cómo Verificar Seguridad

### Backend

1. **SQL Injection**: Prueba con `' OR '1'='1`
   - ✅ Backend rechaza (no es match de regex)
   - ✅ No devuelve datos sensibles

2. **XSS**: Prueba con `<script>alert('xss')</script>`
   - ✅ Frontend lo escapa
   - ✅ Se renderiza como texto

3. **Password**: Verifica en `expenses.db`
   - ✅ Contraseña hasheada (no legible)
   - ✅ Salt único

### Frontend

1. **XSS**: Inspecciona DevTools → Network
   - ✅ Payloads aparecen escapados
   - ✅ No se ejecutan scripts

2. **CORS**: Prueba request desde dominio distinto
   - ✅ Browser bloquea (CORS)
   - ✅ Error CORS en console

---

## 🛠️ Mantener la Seguridad

### Agregar Validación a Nuevo Campo

1. **Backend** (`backend/utils/validators.py`):
```python
def validate_new_field(value: str) -> str:
    if not isinstance(value, str):
        raise ValidationError("Field debe ser texto")
    # ...
    return value
```

2. **Frontend** (`frontend/js/security.js`):
```javascript
function validateNewField(field) {
    if (!/^[valid-pattern]$/i.test(field)) {
        return { valid: false, error: 'Mensaje' };
    }
    return { valid: true };
}
```

3. **Usar en formulario** (`frontend/js/app.js`):
```javascript
const validation = validateFormData(data, [
    { name: 'newField', type: 'newField' }
]);
```

### Agregar Nueva Ruta en Backend

1. Crear en `backend/app.py`
2. Validar entrada
3. Usar parámetros preparados
4. Retornar error genérico si falla

```python
@app.route('/api/new-endpoint', methods=['POST'])
def new_endpoint():
    try:
        data = request.get_json()
        # Validar
        value = validate_field(data.get('field'))
        # Usar parámetros preparados
        c.execute('SELECT * FROM table WHERE field = ?', (value,))
        return jsonify(...), 200
    except ValidationError as e:
        return jsonify({'error': str(e)}), 400
```

---

## 📋 Checklist de Seguridad

- [ ] Todas las entradas se validan (client + server)
- [ ] SQL usa parámetros preparados
- [ ] Contraseñas están hasheadas (PBKDF2)
- [ ] Errores no exponen detalles internos
- [ ] CORS está restringido
- [ ] Headers de seguridad están presentes
- [ ] XSS está prevenido (escapado)
- [ ] Modulación de código clara
- [ ] Logging de errores activo
- [ ] Tests de seguridad pasados

---

## 🔐 En Producción

### IMPORTANTE:

1. **HTTPS**: Usar SSL/TLS siempre
2. **Environment Variables**: Guardar secrets en .env
3. **Rate Limiting**: Implementar límites de requests
4. **CSRF Tokens**: Agregar protección CSRF
5. **Logging**: Monitorear accesos y errores
6. **WAF**: Usar Web Application Firewall
7. **Backups**: Encriptar backups de DB
8. **Updates**: Mantener dependencias actualizadas

---

## 📞 Reportar Issues

Si encuentras un problema de seguridad:
1. NO lo publiques en redes
2. Contacta a través de email seguro
3. Proporciona detalles de cómo reproducirlo
4. Espera confirmación antes de publicar

---

**Ultima actualización:** 2026-02-01
**Status:** ✅ Secure
