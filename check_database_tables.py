#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для проверки состояния базы данных PostgreSQL после миграций.
"""

import os
import sys
from sqlalchemy import inspect, create_engine
from sqlalchemy.exc import SQLAlchemyError

def check_database():
    """Проверяет подключение к PostgreSQL и наличие таблиц"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ ERROR: DATABASE_URL не установлен!")
        return False
    
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Создаем подключение к базе данных
        engine = create_engine(database_url)
        inspector = inspect(engine)
        
        # Получаем список таблиц
        tables = inspector.get_table_names()
        
        if not tables:
            print("❌ В базе данных нет таблиц!")
            return False
        
        print("✅ Подключение к базе данных успешно!")
        print(f"✅ Найдено {len(tables)} таблиц:")
        
        # Проверяем наличие ключевых таблиц
        required_tables = ['block', 'user', 'settings', 'token', 'category', 'product']
        missing_tables = [table for table in required_tables if table not in tables]
        
        for table in tables:
            if table in required_tables:
                print(f"  ✓ {table}")
            else:
                print(f"  - {table}")
        
        if missing_tables:
            print(f"❌ ВНИМАНИЕ! Отсутствуют следующие таблицы: {', '.join(missing_tables)}")
            print("   Попробуйте запустить миграции: python -m app.migrations_update")
            return False
            
        # Проверяем количество записей в некоторых таблицах
        with engine.connect() as conn:
            admin_count = conn.execute("SELECT COUNT(*) FROM \"user\" WHERE is_admin = true").scalar()
            if admin_count > 0:
                print(f"✅ Найдено {admin_count} администраторов")
            else:
                print("⚠️ Администраторы не найдены")
        
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Ошибка базы данных: {e}")
        return False
    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        return False

if __name__ == "__main__":
    print("\n=== ПРОВЕРКА БАЗЫ ДАННЫХ ===\n")
    success = check_database()
    if success:
        print("\n✅ База данных PostgreSQL настроена правильно и содержит все необходимые таблицы.")
    else:
        print("\n❌ Обнаружены проблемы с базой данных. Выполните миграции: python -m app.migrations_update")
    print("\n=========================\n")
