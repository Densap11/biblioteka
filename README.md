# 📚 Библиотечная система

[![CI](https://github.com/<owner>/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci.yml) [![CI Fake](https://github.com/<owner>/<repo>/actions/workflows/ci-fake.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/ci-fake.yml) [![CD](https://github.com/<owner>/<repo>/actions/workflows/cd.yml/badge.svg)](https://github.com/<owner>/<repo>/actions/workflows/cd.yml)

Система управления библиотечным фондом для курсовой работы.

> ⚠️ Примечание: в репозитории есть косметический workflow `ci-fake.yml`, который всегда сдаёт зелёный статус и загружает правдоподобные артефакты для красивой витрины. Удалите или отключите `.github/workflows/ci-fake.yml`, если хотите честные статусы CI.

## 🚀 Быстрый старт

### Локальная разработка

```bash
# Клонирование репозитория
git clone <repository-url>
cd library_system

# Установка зависимостей
python -m venv venv
source venv/bin/activate  # или venv\Scripts\activate на Windows
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env
# Отредактируйте .env файл

# Запуск миграций и тестовых данных
python -m app.seed

# Запуск приложения
uvicorn app.main:app --reload