#!/bin/bash
# scripts/run-tests.sh

echo "🧪 Запуск тестов..."

# Создаем тестовую базу данных
export DATABASE_URL="sqlite:///./test.db"
export SECRET_KEY="test-secret-key"

# Запускаем тесты
pytest tests/ -v \
    --cov=app \
    --cov-report=term-missing \
    --cov-report=html \
    --cov-report=xml \
    --junitxml=test-results.xml

# Сохраняем результат
test_result=$?

# Генерируем отчет о покрытии
if [ -f "coverage.xml" ]; then
    echo "📊 Покрытие кода тестами:"
    python -c "
import xml.etree.ElementTree as ET
tree = ET.parse('coverage.xml')
root = tree.getroot()
coverage = root.attrib['line-rate']
print(f'✅ Покрытие: {float(coverage)*100:.2f}%')
"
fi

# Очищаем тестовую базу данных
rm -f test.db

exit $test_result