FROM python:3.9-slim

# Установка зависимостей для PostgreSQL
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt requirements.txt

# Установка Python-библиотек
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY dmp.py dmp.py

# Команда запуска
CMD ["python", "dmp.py"]
