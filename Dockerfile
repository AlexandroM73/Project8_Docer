FROM python:3.11-slim

WORKDIR /app

# Системные зависимости для psycopg2 и сборки пакетов
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка зависимостей проекта
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего кода проекта
COPY . .

# ЗАПУСК ЧЕРЕЗ GUNICORN (вместо runserver)
# config.wsgi:application — точно соответствует твоему файлу config/wsgi.py
# --bind 0.0.0.0:8000 — слушает все интерфейсы на порту 8000
# --workers 3 — запускает 3 рабочих процесса для параллельной обработки запросов
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
