#!/bin/bash
# prestart.sh - Runs before app startup on Render

echo "=== ПРЕДСТАРТОВАЯ ПРОВЕРКА ==="

# Диагностика окружения
echo "Проверка переменных окружения..."
if [ -z "$DATABASE_URL" ]; then
    echo "ВНИМАНИЕ: DATABASE_URL не установлен!"
else
    echo "DATABASE_URL установлен."
    
    # Проверить, не содержит ли URL localhost
    if [[ "$DATABASE_URL" == *"localhost"* ]] || [[ "$DATABASE_URL" == *"127.0.0.1"* ]]; then
        echo "ОШИБКА: DATABASE_URL содержит localhost, что не будет работать на Render!"
    fi
fi

# Проверка на установленные пакеты
echo "Проверка необходимых пакетов..."
pip list | grep psycopg2

# Попытаться запустить миграции
echo "Выполнение миграций базы данных..."
python -m app.migrations_update

echo "=== ПРЕДСТАРТОВАЯ ПРОВЕРКА ЗАВЕРШЕНА ==="
