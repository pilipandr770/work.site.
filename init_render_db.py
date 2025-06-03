#!/usr/bin/env python
# init_render_db.py

"""
Скрипт для инициализации базы данных на Render.com.
Запускайте этот скрипт после деплоя, чтобы создать таблицы в PostgreSQL.
"""

import os
import sys
from pathlib import Path

def setup_environment():
    """Set up the environment for database initialization."""
    print("Настройка окружения...")
    
    # Add the current directory to Python path
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        env_path = current_dir / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Переменные окружения загружены из {env_path}")
    except ImportError:
        print("Предупреждение: python-dotenv не установлен")
    
    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        db_type = "PostgreSQL" if "postgres" in db_url else "SQLite"
        print(f"Найдена строка подключения к базе данных ({db_type})")
    else:
        print("Предупреждение: DATABASE_URL не найден в переменных окружения")

def run_migrations():
    """Run database migrations to create or update tables."""
    print("\nЗапуск миграций базы данных...")
    
    try:
        from app.migrations_update import upgrade_database
        
        # Run the migrations
        upgrade_database()
        print("✅ Миграции успешно выполнены!")
        return True
    except Exception as e:
        print(f"❌ Ошибка при выполнении миграций: {e}")
        return False

def verify_tables():
    """Verify that database tables exist."""
    print("\nПроверка созданных таблиц...")
    
    try:
        # Import the database connection
        from app import create_app, db
        
        # Create a temporary application context
        with create_app().app_context():
            # Run a query to get table names
            engine = db.engine
            inspector = db.inspect(engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✅ Найдено {len(tables)} таблиц в базе данных:")
                for table in tables:
                    print(f"  - {table}")
                return True
            else:
                print("❌ В базе данных не найдено таблиц!")
                return False
    except Exception as e:
        print(f"❌ Ошибка при проверке таблиц: {e}")
        return False

def main():
    """Run the database initialization process."""
    print("=" * 50)
    print("ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ НА RENDER.COM")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Run migrations
    migrations_success = run_migrations()
    
    # Verify tables
    if migrations_success:
        tables_success = verify_tables()
    else:
        tables_success = False
    
    print("\n" + "=" * 50)
    if migrations_success and tables_success:
        print("✅ ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ УСПЕШНО ЗАВЕРШЕНА!")
        print("Теперь ваше приложение должно работать корректно.")
    else:
        print("❌ ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ ЗАВЕРШИЛАСЬ С ОШИБКАМИ")
        print("Пожалуйста, проверьте логи выше для выявления причин.")
    print("=" * 50)

if __name__ == "__main__":
    main()
