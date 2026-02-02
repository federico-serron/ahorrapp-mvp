FROM python:3.12-slim

WORKDIR /app

# Copiar requirements e instalar
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar solo el backend al contenedor
COPY backend/ /app/backend

# Establecer directorio de trabajo en backend
WORKDIR /app/backend

# Variables de entorno
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Exponer puerto
EXPOSE 8000
# Instalar Gunicorn y usar el WSGI entrypoint
RUN pip install --no-cache-dir gunicorn

# Exponer puerto y arrancar con gunicorn usando $PORT
CMD ["sh", "-c", "gunicorn -w 4 -b 0.0.0.0:${PORT:-8000} wsgi:app"]
