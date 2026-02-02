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

# Comando de inicio
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
