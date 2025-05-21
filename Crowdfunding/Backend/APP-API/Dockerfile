# Imagen base con Python y soporte para WeasyPrint
FROM python:3.13-slim

# Instala dependencias del sistema para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    curl \
    && apt-get clean

# Crea el directorio de la app
WORKDIR /app

# Copia los archivos del proyecto
COPY . /app

# Instala dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expón el puerto del servidor Django
EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
