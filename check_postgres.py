"""
Скрипт для проверки подключения к PostgreSQL и создания базы данных.
"""
import os
import psycopg2
from urllib.parse import urlparse

# Чтение переменных окружения из .env файла
def load_dotenv():
    with open('.env', 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Загружаем переменные из .env
load_dotenv()

# Получаем DATABASE_URL
database_url = os.environ.get('DATABASE_URL')
print(f"DATABASE_URL: {database_url}")

if not database_url:
    print("❌ DATABASE_URL не найден в переменных окружения!")
    exit(1)

# Парсим URL для получения компонентов подключения
try:
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        print(f"✅ Скорректированный URL: {database_url}")
    
    result = urlparse(database_url)
    username = result.username
    password = result.password
    host = result.hostname
    port = result.port or 5432  # Default port is 5432
    database = result.path[1:]  # Remove leading '/'
    
    print(f"\nАнализ строки подключения:")
    print(f"Пользователь: {username}")
    print(f"Пароль: {'*' * len(password) if password else 'не задан'}")
    print(f"Хост: {host}")
    print(f"Порт: {port}")
    print(f"База данных: {database}")
    
    # Сначала попробуем подключиться к postgres (системная БД)
    print("\nПопытка подключения к PostgreSQL (системная БД postgres)...")
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database='postgres'
        )
        conn.autocommit = True
        print("✅ Подключение к системной БД postgres успешно!")
        
        # Проверяем, существует ли наша БД
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (database,))
            exists = cur.fetchone()
            
            if exists:
                print(f"✅ База данных {database} уже существует")
            else:
                print(f"❌ База данных {database} не найдена, создаем...")
                try:
                    # Создаем БД (safe создание - только если не существует)
                    cur.execute(f"CREATE DATABASE {database};")
                    print(f"✅ База данных {database} успешно создана!")
                except Exception as e:
                    print(f"❌ Ошибка при создании БД: {e}")
        
        conn.close()
        
        # Теперь подключаемся к нашей базе
        print(f"\nПопытка подключения к базе {database}...")
        try:
            app_conn = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            print(f"✅ Подключение к базе {database} успешно!")
            app_conn.close()
        except Exception as e:
            print(f"❌ Ошибка при подключении к базе {database}: {e}")
        
    except Exception as e:
        print(f"❌ Ошибка при подключении к PostgreSQL: {e}")
        print("\nВозможные причины:")
        print("1. PostgreSQL не запущен на указанном хосте и порту")
        print("2. Неверные имя пользователя или пароль")
        print("3. Пользователю не разрешено подключаться с указанного IP-адреса")
        print("4. Брандмауэр блокирует подключения")
        
except Exception as e:
    print(f"❌ Ошибка парсинга DATABASE_URL: {e}")
