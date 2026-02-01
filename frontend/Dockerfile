FROM python:3.12-slim

WORKDIR /app

COPY index.html .
COPY server.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 3000

CMD ["python", "server.py"]
