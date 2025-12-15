# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЕ файлы проекта
COPY . .

# Проверяем, что шаблоны существуют
RUN if [ ! -d "templates" ]; then mkdir templates; fi
RUN if [ ! -f "templates/index.html" ]; then echo "<h1>Библиотечная система</h1>" > templates/index.html; fi

# Открываем порт
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]