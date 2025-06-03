#!/usr/bin/env python
# debug_render_db.py

"""
Отладочный скрипт для проверки подключения к базе данных на Render.com
"""

import os
import sys

def print_heading(text):
    """Print a section heading"""
    print("\n" + "=" * 50)
    print(text)
    print("=" * 50)

def main():
    print_heading("ДИАГНОСТИКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
    
    # Проверить переменную DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        # Скрыть пароль для безопасности
        masked_url = db_url
        if '@' in masked_url:
            parts = masked_url.split('@')
            auth = parts[0].split('://')
            masked_url = f"{auth[0]}://****:****@{parts[1]}"
        print(f"DATABASE_URL установлена: {masked_url}")
        
        # Проверить, не использует ли URL localhost
        if 'localhost' in db_url or '127.0.0.1' in db_url:
            print("ОШИБКА: DATABASE_URL содержит 'localhost' или '127.0.0.1'!")
            print("На Render.com это не будет работать, так как PostgreSQL должен быть внешним.")
    else:
        print("ОШИБКА: Переменная DATABASE_URL не установлена!")
        
    # Проверить, работаем ли мы на Render.com
    is_render = 'RENDER' in os.environ
    print(f"Работаем на Render.com: {'Да' if is_render else 'Нет'}")
    
    # Попытаться импортировать psycopg2 для PostgreSQL
    try:
        import psycopg2
        print("psycopg2 установлен: Да")
    except ImportError:
        print("ОШИБКА: psycopg2 не установлен! Выполните 'pip install psycopg2-binary'")
        return
    
    # Попытаться подключиться к БД, если есть DATABASE_URL
    if db_url:
        print_heading("ПОПЫТКА ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
        try:
            conn = psycopg2.connect(db_url)
            print("✅ Успешное подключение к базе данных!")
            
            # Получить информацию о БД
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"Версия PostgreSQL: {version}")
            
            # Список таблиц
            cursor.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()
            
            if tables:
                print("\nТаблицы в базе данных:")
                for table in tables:
                    print(f"- {table[0]}")
            else:
                print("\nВ базе данных нет таблиц. Возможно, требуется выполнить миграции.")
            
            cursor.close()
            conn.close()
        except Exception as e:
            print(f"ОШИБКА подключения к базе данных: {e}")
            print("\nВозможные причины:")
            print("1. Неправильный URL базы данных")
            print("2. База данных не создана")
            print("3. Нет сетевого доступа к базе данных")
    
    print_heading("РЕКОМЕНДАЦИИ")
    print("1. На Render.com используйте PostgreSQL из раздела Databases")
    print("2. Убедитесь, что DATABASE_URL в переменных среды указывает на базу Render")
    print("3. Проверьте, что startCommand в render.yaml соответствует Procfile")
    print("4. После настройки базы данных выполните миграции:")
    print("   python -m app.migrations_update")

if __name__ == "__main__":
    main()
