FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias (si aplica)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requirements (desde el contexto raíz)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el backend dentro del contenedor
COPY backend/ /app/backend

# Establecer directorio de trabajo en backend
WORKDIR /app/backend

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production
ENV FLASK_APP=app.py

EXPOSE 8000
# Instalar Gunicorn para producción y usar PORT de la plataforma
RUN pip install --no-cache-dir gunicorn

# Usar gunicorn y respetar la variable $PORT (por ejemplo Railway)
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} wsgi:app"]
