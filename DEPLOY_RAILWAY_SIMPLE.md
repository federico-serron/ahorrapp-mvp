# 🚀 Deploy en Railway - Simple

## Paso 1: Preparar GitHub

```bash
cd /home/pepe/expense-tracker

# Inicializar repo
git init
git add .
git commit -m "Expense Tracker MVP"
git branch -M main

# Crear repo en GitHub y pushear
git remote add origin https://github.com/TU_USUARIO/expense-tracker.git
git push -u origin main
```

## Paso 2: Deploy en Railway

1. Entra a **https://railway.app**
2. Click en **"New Project"**
3. Click en **"Deploy from GitHub"**
4. Selecciona tu repo `expense-tracker`
5. Railway auto-detecta Dockerfile y despliega

## Paso 3: Configurar Variables (Opcional)

En Railway Dashboard → Variables:
```
FLASK_ENV=production
ANTHROPIC_API_KEY=tu_api_key
```

## ✅ ¡Listo!

Tu URL en vivo: `https://expense-tracker-xxxxx.up.railway.app`

---

**Para nuevos deploys: Solo hace `git push` y Railway actualiza automático!**
