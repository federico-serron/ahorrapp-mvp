# 🐳 Docker Setup - Expense Tracker

## 📋 Prerequisitos

- Docker instalado: https://www.docker.com/products/docker-desktop
- DockerHub account: https://hub.docker.com
- Git instalado

## 🚀 Paso 1: Build local y push a DockerHub

### 1.1 Login en DockerHub

```bash
docker login
# Ingresa tu usuario y contraseña de DockerHub
```

### 1.2 Build de las imágenes

```bash
cd /home/pepe/expense-tracker

# Backend
docker build -t TU_USUARIO_DOCKERHUB/expense-tracker-backend:latest ./backend
docker build -t TU_USUARIO_DOCKERHUB/expense-tracker-backend:v1.0 ./backend

# Frontend
docker build -t TU_USUARIO_DOCKERHUB/expense-tracker-frontend:latest ./frontend
docker build -t TU_USUARIO_DOCKERHUB/expense-tracker-frontend:v1.0 ./frontend
```

### 1.3 Push a DockerHub

```bash
# Backend
docker push TU_USUARIO_DOCKERHUB/expense-tracker-backend:latest
docker push TU_USUARIO_DOCKERHUB/expense-tracker-backend:v1.0

# Frontend
docker push TU_USUARIO_DOCKERHUB/expense-tracker-frontend:latest
docker push TU_USUARIO_DOCKERHUB/expense-tracker-frontend:v1.0
```

**Ahora tus imágenes están en DockerHub!**

## 🎯 Paso 2: Usar docker-compose para ejecutar todo

### 2.1 Configurar variable de entorno

```bash
cd /home/pepe/expense-tracker

# En Linux/Mac
export DOCKER_USERNAME="tu_usuario_dockerhub"

# En Windows (PowerShell)
$env:DOCKER_USERNAME="tu_usuario_dockerhub"
```

### 2.2 Ejecutar con docker-compose

```bash
# Descargar imágenes y levantar servicios
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f

# Ver estado de servicios
docker-compose ps

# Acceder a la app
# Frontend: http://localhost:3000
# Backend: http://localhost:5001
```

### 2.3 Detener servicios

```bash
docker-compose down

# Con limpieza de volúmenes (borra base de datos)
docker-compose down -v
```

## 📝 Archivo .env (Opcional)

Crea `.env.docker`:

```env
DOCKER_USERNAME=tu_usuario
FLASK_ENV=production
PORT=5001
```

Luego:

```bash
docker-compose --env-file .env.docker up -d
```

## 🔧 Comandos útiles

```bash
# Ver logs de un servicio específico
docker-compose logs backend
docker-compose logs frontend

# Ejecutar comando dentro del contenedor
docker-compose exec backend python -c "import sqlite3; print(sqlite3.connect('expenses.db'))"

# Rebuild sin caché
docker-compose up -d --build --no-cache

# Ver volúmenes
docker volume ls

# Limpiar todo (contenedores, imágenes, volúmenes)
docker-compose down -v
docker system prune -a
```

## 🐛 Troubleshooting

### Puerto ya en uso

```bash
# Listar puertos
netstat -tuln | grep -E "3000|5001"

# O cambiar puerto en docker-compose.yml
# ports: "8080:3000"  # Ahora accede a http://localhost:8080
```

### Contenedor no inicia

```bash
# Ver logs detallados
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose down
docker-compose up -d --build
```

### Permisos en base de datos

```bash
# Dar permisos a la carpeta
chmod 777 ./backend/expenses.db
```

## ✅ Checklist Final

- [ ] Docker instalado y corriendo
- [ ] DockerHub cuenta creada
- [ ] `docker login` ejecutado
- [ ] Imágenes buildadas localmente
- [ ] Imágenes pusheadas a DockerHub
- [ ] `docker-compose up -d` ejecutado
- [ ] Acceso a http://localhost:3000 funciona
- [ ] Backend responde en http://localhost:5001

## 🎉 ¡Listo!

Tu app está en Docker. Ahora puede correr en cualquier máquina con:

```bash
export DOCKER_USERNAME="tu_usuario"
docker-compose up -d
```

---

**Próximo paso: Deploy en VPS o Railway con Docker**
