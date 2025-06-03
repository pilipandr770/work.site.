"""
Скрипт для детальной проверки подключения к PostgreSQL 
с выводом всех возможных ошибок.
"""
import os
import sys
import time
from urllib.parse import urlparse

try:
    import psycopg2
    print("✅ psycopg2 установлен")
except ImportError:
    print("❌ psycopg2 не установлен")
    print("Установите его командой: pip install psycopg2-binary")
    sys.exit(1)

def test_connection(url):
    """Тестирует подключение к PostgreSQL с полной отладочной информацией"""
    
    # Проверяем URL
    print(f"\nПроверка URL: {url}")
    if not url.startswith('postgresql://'):
        print("❌ Неверный формат URL. Должно начинаться с 'postgresql://'")
        return False
    
    # Парсим URL
    try:
        result = urlparse(url)
        username = result.username
        password = result.password
        host = result.hostname
        port = result.port or 5432
        dbname = result.path[1:] if result.path else None
        
        print("\nАнализ строки подключения:")
        print(f"Пользователь: {username}")
        print(f"Пароль: {'*' * len(password) if password else 'не задан'}")
        print(f"Хост: {host}")
        print(f"Порт: {port}")
        print(f"База данных: {dbname}")
        
        # Проверяем параметры
        if not username:
            print("❌ Имя пользователя не указано")
            return False
        
        if not password:
            print("❌ Пароль не указан")
            return False
        
        if not host:
            print("❌ Хост не указан")
            return False
        
        if not dbname:
            print("❌ Имя базы данных не указано")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при парсинге URL: {e}")
        return False
    
    # Проверяем доступность хоста и порта
    import socket
    try:
        print(f"\nПроверка доступности {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print(f"✅ Порт {port} открыт на {host}")
        else:
            print(f"❌ Порт {port} закрыт на {host}. PostgreSQL не запущен или недоступен.")
            return False
    except Exception as e:
        print(f"❌ Ошибка при проверке доступности: {e}")
        return False
    
    # Пробуем подключиться
    try:
        print("\nПодключение к PostgreSQL...")
        conn_params = {
            'user': username,
            'password': password,
            'host': host,
            'port': port,
            'dbname': dbname,
            'connect_timeout': 5
        }
        
        # Пробуем подключиться к системной БД postgres
        print("\n1. Проверка доступа к системной базе postgres...")
        postgres_conn_params = conn_params.copy()
        postgres_conn_params['dbname'] = 'postgres'
        
        try:
            conn = psycopg2.connect(**postgres_conn_params)
            conn.autocommit = True
            print("✅ Подключение к postgres успешно!")
            
            # Проверяем наличие указанной БД
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (dbname,))
            exists = cur.fetchone()
            
            if exists:
                print(f"✅ База данных {dbname} существует")
            else:
                print(f"❌ База данных {dbname} не существует")
                
                # Пробуем создать базу
                try:
                    cur.execute(f"CREATE DATABASE {dbname} WITH OWNER {username};")
                    print(f"✅ База данных {dbname} успешно создана")
                except Exception as e:
                    print(f"❌ Ошибка при создании базы данных: {e}")
                
            cur.close()
            conn.close()
        except Exception as e:
            print(f"❌ Ошибка подключения к системной БД: {e}")
        
        # Пробуем подключиться к указанной БД
        print(f"\n2. Подключение к базе {dbname}...")
        try:
            conn = psycopg2.connect(**conn_params)
            print(f"✅ Подключение к {dbname} успешно!")
            
            # Проверяем версию PostgreSQL
            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()
            print(f"\nВерсия PostgreSQL: {version[0]}")
            
            # Проверяем схему
            cur.execute("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema='public'
            """)
            tables = cur.fetchall()
            
            if tables:
                print(f"\nТаблицы в базе данных {dbname}:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print(f"\nВ базе {dbname} нет таблиц")
                print("Возможно, нужно запустить миграции: python -m app.migrations_update")
            
            cur.close()
            conn.close()
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к {dbname}: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Общая ошибка подключения: {e}")
        return False

def read_env():
    """Читает .env файл и возвращает DATABASE_URL"""
    try:
        with open(".env", "r") as f:
            for line in f:
                if line.strip().startswith("DATABASE_URL="):
                    url = line.strip().split("=", 1)[1]
                    return url
    except Exception as e:
        print(f"❌ Ошибка чтения .env файла: {e}")
    return None

def main():
    print("=" * 60)
    print("ДЕТАЛЬНАЯ ПРОВЕРКА POSTGRESQL")
    print("=" * 60)
    
    # Пробуем получить URL из .env
    url = read_env()
    if url and url.startswith('postgresql://'):
        print(f"Найден URL в .env: {url}")
    else:
        url = input("\nВведите URL подключения к PostgreSQL\n(например, postgresql://flask:flask_password@localhost:5433/ittoken_db): ")
    
    if not url:
        print("❌ URL не указан")
        return
    
    # Тестируем подключение
    success = test_connection(url)
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ПРОВЕРКА УСПЕШНО ЗАВЕРШЕНА!")
        print("Вы можете использовать PostgreSQL с вашим приложением")
    else:
        print("❌ ОБНАРУЖЕНЫ ПРОБЛЕМЫ С ПОДКЛЮЧЕНИЕМ")
        print("Исправьте указанные ошибки и запустите скрипт снова")
    print("=" * 60)

if __name__ == "__main__":
    main()
