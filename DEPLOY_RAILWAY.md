# 🚀 Deploy en Railway.app

## Paso 1: Preparar GitHub

1. Crea una cuenta en GitHub (si no tienes)
2. Crea un nuevo repositorio llamado `expense-tracker`
3. Abre terminal en tu computadora:

```bash
cd /home/pepe/expense-tracker
git init
git add .
git commit -m "Expense Tracker MVP"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/expense-tracker.git
git push -u origin main
```

## Paso 2: Conectar Railway.app

1. Entra a https://railway.app
2. Click en "Dashboard"
3. Click en "New Project"
4. Click en "Deploy from GitHub"
5. Selecciona el repo `expense-tracker`
6. Railway auto-detecta Dockerfile
7. Espera a que se despliegue (2-3 minutos)

## Paso 3: Configurar Variables de Entorno

En Railway Dashboard:
1. Click en tu proyecto
2. Click en "Variables"
3. Agrega:
   ```
   FLASK_ENV = production
   PORT = 8000
   ANTHROPIC_API_KEY = tu_api_key
   ```

## Paso 4: Tu URL en vivo

Railway te generará automáticamente:
```
https://expense-tracker-production.up.railway.app
```

(La URL exacta aparecerá en tu dashboard)

## ✅ Listo!

Tu app está en línea. Comparte el link y ¡a presentar!
