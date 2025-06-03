"""
Скрипт для диагностики и создания базы данных PostgreSQL.
Шаг за шагом проверяет и решает все проблемы для подключения к PostgreSQL.
"""
import os
import sys
import subprocess
import socket
import time
import getpass

try:
    import psycopg2
    from psycopg2 import sql
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    print("✅ Библиотека psycopg2 успешно импортирована")
except ImportError:
    print("❌ Библиотека psycopg2 не установлена. Устанавливаем...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "psycopg2-binary"])
        import psycopg2
        from psycopg2 import sql
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        print("✅ psycopg2-binary успешно установлена")
    except Exception as e:
        print(f"❌ Не удалось установить psycopg2-binary: {e}")
        sys.exit(1)

def load_env_vars():
    """Загружает переменные окружения из .env файла"""
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
                    except ValueError:
                        pass
        return env_vars
    except Exception as e:
        print(f"❌ Ошибка при чтении .env файла: {e}")
        return {}

def check_postgres_running(host, port):
    """Проверяет, доступен ли PostgreSQL на указанном хосте и порту"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"❌ Ошибка при проверке соединения: {e}")
        return False

def create_database(host, port, user, password, dbname):
    """Создает базу данных PostgreSQL если она не существует"""
    try:
        # Подключаемся к системной БД postgres
        print(f"Пытаемся подключиться к PostgreSQL для создания базы данных {dbname}...")
        
        # Сначала проверяем доступность сервера
        if not check_postgres_running(host, port):
            print(f"❌ PostgreSQL не запущен или недоступен на {host}:{port}")
            return False
            print("❌ DATABASE_URL не найден или не указывает на PostgreSQL")
            print(f"   Текущий DATABASE_URL: {database_url}")
            return False
        
        # Парсим URL для извлечения компонентов
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        parsed_url = urlparse(database_url)
        db_name = parsed_url.path[1:]  # Убираем начальный слеш
        username = parsed_url.username
        password = parsed_url.password
        host = parsed_url.hostname
        port = parsed_url.port or 5432
        
        print(f"Параметры подключения:")
        print(f"Хост: {host}")
        print(f"Порт: {port}")
        print(f"Пользователь: {username}")
        print(f"База данных: {db_name}")
        
        # Подключаемся к системной БД postgres для создания нашей БД
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database='postgres'
        )
        conn.autocommit = True
        
        # Проверяем, существует ли база данных
        with conn.cursor() as cur:
            cur.execute(f"SELECT 1 FROM pg_database WHERE datname = %s;", (db_name,))
            exists = cur.fetchone()
            
            if exists:
                print(f"✅ База данных {db_name} уже существует")
            else:
                print(f"🔄 База данных {db_name} не найдена, создаем...")
                try:
                    # Создаем БД
                    cur.execute(f"CREATE DATABASE {db_name};")
                    print(f"✅ База данных {db_name} успешно создана!")
                except Exception as e:
                    print(f"❌ Ошибка при создании БД: {e}")
                    return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def initialize_tables():
    """Инициализирует таблицы базы данных"""
    try:
        # Импортируем после создания базы данных, чтобы использовать правильный URL
        from app import create_app, db
        from app.models import User
        from werkzeug.security import generate_password_hash
        
        print("\n🔄 Инициализация таблиц базы данных...")
        
        app = create_app()
        with app.app_context():
            # Создаем все таблицы
            db.create_all()
            print("✅ Таблицы базы данных созданы")
            
            # Проверяем наличие администратора
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Создан администратор (логин: admin, пароль: admin)")
            else:
                print("✅ Администратор уже существует")
                
        return True
    except Exception as e:
        print(f"❌ Ошибка инициализации таблиц: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Настройка PostgreSQL для проекта IT Token ===\n")
    
    # Загружаем переменные окружения
    load_env_vars()
    
    # Проверяем, что используется PostgreSQL
    database_url = os.environ.get('DATABASE_URL', '')
    if not database_url.startswith('postgresql'):
        print("❌ Настройте DATABASE_URL для использования PostgreSQL в файле .env")
        print("   Например: DATABASE_URL=postgresql://postgres:password@localhost:5433/ittoken_db")
        sys.exit(1)
    
    # Создаем базу данных
    if create_database():
        # Инициализируем таблицы
        if initialize_tables():
            print("\n✅ PostgreSQL успешно настроен для проекта!")
            print("\nТеперь вы можете запустить приложение командой:")
            print("python -m app.run")
        else:
            print("\n❌ Не удалось инициализировать таблицы. Проверьте предыдущие сообщения об ошибках.")
    else:
        print("\n❌ Не удалось создать базу данных. Проверьте настройки PostgreSQL.")
