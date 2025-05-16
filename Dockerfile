FROM python:3.11-slim

# Evitar interacciones y mejorar logs
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Instalar librerías del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libjpeg-dev \
    libpng-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-liberation \
    fonts-dejavu \
    wget \
    curl \
    git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Instalar dependencias Python
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Arranca Gunicorn (4 workers) en el puerto 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
