#!/bin/bash
# scripts/ci-check.sh

echo "🔍 Запуск проверок CI/CD..."

# Проверка структуры проекта
echo "1. Проверка структуры проекта..."
required_dirs=("app" "tests" "templates")
required_files=("requirements.txt" "Dockerfile" "docker-compose.yml")

for dir in "${required_dirs[@]}"; do
    if [ ! -d "$dir" ]; then
        echo "❌ Отсутствует директория: $dir"
        exit 1
    fi
done

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Отсутствует файл: $file"
        exit 1
    fi
done

echo "✅ Структура проекта корректна"

# Проверка Python зависимостей
echo "2. Проверка Python зависимостей..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден"
    exit 1
fi

echo "✅ requirements.txt найден"

# Проверка Dockerfile
echo "3. Проверка Dockerfile..."
if ! grep -q "FROM python" Dockerfile; then
    echo "❌ Dockerfile должен начинаться с FROM python"
    exit 1
fi

if ! grep -q "requirements.txt" Dockerfile; then
    echo "❌ Dockerfile должен копировать requirements.txt"
    exit 1
fi

echo "✅ Dockerfile корректный"

# Проверка docker-compose.yml
echo "4. Проверка docker-compose.yml..."
if ! grep -q "services:" docker-compose.yml; then
    echo "❌ docker-compose.yml должен содержать секцию services"
    exit 1
fi

echo "✅ docker-compose.yml корректный"

# Проверка тестов
echo "5. Проверка тестов..."
if [ ! -d "tests" ]; then
    echo "⚠️  Директория tests не найдена"
else
    test_count=$(find tests -name "test_*.py" | wc -l)
    if [ "$test_count" -eq 0 ]; then
        echo "⚠️  Тесты не найдены"
    else
        echo "✅ Найдено $test_count тестов"
    fi
fi

echo "🎉 Все проверки CI/CD пройдены успешно!"