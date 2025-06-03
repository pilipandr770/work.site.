"""
Скрипт для создания базы данных PostgreSQL и пользователя.
"""
import subprocess
import sys
import getpass

def create_postgres_user_db():
    print("=== Создание пользователя и базы данных PostgreSQL ===")
    
    # Запрашиваем администраторский пароль для PostgreSQL
    admin_password = getpass.getpass("Введите пароль администратора PostgreSQL: ")
    
    # Команда для создания пользователя и базы данных
    create_user_cmd = [
        "C:\\Program Files\\PostgreSQL\\17\\bin\\psql",
        "-h", "localhost",
        "-p", "5433",
        "-U", "postgres",
        "-c", "CREATE USER flask WITH PASSWORD 'flask_password';",
        "-w"
    ]
    
    create_db_cmd = [
        "C:\\Program Files\\PostgreSQL\\17\\bin\\psql",
        "-h", "localhost",
        "-p", "5433",
        "-U", "postgres",
        "-c", "CREATE DATABASE ittoken_db WITH OWNER flask;",
        "-w"
    ]
    
    grant_cmd = [
        "C:\\Program Files\\PostgreSQL\\17\\bin\\psql",
        "-h", "localhost",
        "-p", "5433",
        "-U", "postgres",
        "-c", "GRANT ALL PRIVILEGES ON DATABASE ittoken_db TO flask;",
        "-w"
    ]
    
    env = {"PGPASSWORD": admin_password}
    
    try:
        # Создаем пользователя
        print("\nСоздание пользователя 'flask'...")
        result = subprocess.run(create_user_cmd, env=env, capture_output=True, text=True)
        if "ERROR" in result.stderr:
            print(f"Ошибка создания пользователя: {result.stderr}")
        else:
            print("✓ Пользователь создан успешно")
        
        # Создаем базу данных
        print("\nСоздание базы данных 'ittoken_db'...")
        result = subprocess.run(create_db_cmd, env=env, capture_output=True, text=True)
        if "ERROR" in result.stderr:
            print(f"Ошибка создания базы данных: {result.stderr}")
        else:
            print("✓ База данных создана успешно")
        
        # Даем права пользователю
        print("\nПредоставление прав...")
        result = subprocess.run(grant_cmd, env=env, capture_output=True, text=True)
        if "ERROR" in result.stderr:
            print(f"Ошибка предоставления прав: {result.stderr}")
        else:
            print("✓ Права предоставлены успешно")
            
        print("\n=== Готово! ===")
        print("Теперь вы можете использовать следующую строку подключения:")
        print("DATABASE_URL=postgresql://flask:flask_password@localhost:5433/ittoken_db")
        
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    create_postgres_user_db()
