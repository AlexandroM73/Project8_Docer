FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# Показываем, что реально в файле
RUN cat requirements.txt && echo "--- Конец файла ---"

# Ставим зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ГАРАНТИРОВАННО ставим pytest-cov (теперь он точно будет в образе)
RUN pip install --no-cache-dir pytest-cov

COPY . .

ENV PYTEST_COV_INSTALL_TRIGGER=202610311600
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
