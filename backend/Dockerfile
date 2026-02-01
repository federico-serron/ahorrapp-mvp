FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=8000"]
