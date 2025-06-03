"""
Скрипт для проверки подключения к PostgreSQL на порту 5433 
с разными комбинациями имени пользователя/пароля.
"""
import psycopg2

def try_connection(host, port, user, password, database="postgres"):
    try:
        print(f"\nПопытка подключения с параметрами:")
        print(f"  Хост:     {host}")
        print(f"  Порт:     {port}")
        print(f"  Польз:    {user}")
        print(f"  Пароль:   {'*' * len(password)}")
        print(f"  БД:       {database}")
        
        conn = psycopg2.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=3
        )
        print("✅ ПОДКЛЮЧЕНИЕ УСПЕШНО!")
        
        # Получаем версию PostgreSQL
        cur = conn.cursor()
        cur.execute('SELECT version();')
        db_version = cur.fetchone()
        print(f"🔍 Версия PostgreSQL: {db_version[0]}")
        
        # Список баз данных
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = cur.fetchall()
        print(f"🔍 Доступные базы данных:")
        for db in databases:
            print(f"   - {db[0]}")
            
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        return False

if __name__ == "__main__":
    print("=== Тестирование подключения к PostgreSQL ===")
    
    # Параметры подключения
    host = "localhost"
    port = 5433
    
    # Список комбинаций логин/пароль для проверки
    credentials = [
        ("postgres", "Dnepr75ok613770"),
        ("postgres", "Dnepr75ok6137707"),
        ("postgres", "postgres"),
        ("postgresql", "postgresql")
    ]
    
    success = False
    for username, password in credentials:
        if try_connection(host, port, username, password):
            success = True
            print(f"\n✅ РАБОТАЮЩАЯ КОМБИНАЦИЯ:")
            print(f"   Пользователь: {username}")
            print(f"   Пароль: {'*' * len(password)}")
            break
    
    if not success:
        print("\n❌ Не удалось подключиться ни с одной из комбинаций.")
        print("   Попробуйте другие учетные данные или убедитесь, что сервер PostgreSQL запущен.")
