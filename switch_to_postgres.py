"""
Скрипт для переключения проекта на PostgreSQL для продакшена.
"""
import os
import sys
from pathlib import Path

def switch_to_postgres():
    """Переключает конфигурацию на PostgreSQL для продакшена"""
    try:
        # Создаем бэкап текущего .env файла
        env_path = Path('.env')
        backup_path = Path('.env.sqlite.backup')
        
        with open(env_path, 'r') as f:
            env_content = f.read()
        
        with open(backup_path, 'w') as f:
            f.write(env_content)
            print(f"✅ Создан бэкап файла .env как {backup_path}")
        
        # Получаем параметры подключения
        db_host = input("Введите хост PostgreSQL (по умолчанию: localhost): ") or "localhost"
        db_port = input("Введите порт PostgreSQL (по умолчанию: 5433): ") or "5433"
        db_user = input("Введите имя пользователя PostgreSQL (по умолчанию: postgres): ") or "postgres"
        db_password = input("Введите пароль PostgreSQL: ")
        if not db_password:
            print("❌ Пароль не может быть пустым")
            return
        db_name = input("Введите имя базы данных (по умолчанию: ittoken_db): ") or "ittoken_db"
        
        # Формируем строку подключения
        db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        # Обновляем .env для использования PostgreSQL
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        with open(env_path, 'w') as f:
            for line in lines:
                # Обновляем DATABASE_URL
                if line.strip().startswith('DATABASE_URL='):
                    f.write(f'DATABASE_URL={db_url}\n')
                # Комментируем строку с SQLite, если она есть
                elif line.strip().startswith('# DATABASE_URL=sqlite:'):
                    f.write(line)
                # Раскомментируем строку с PostgreSQL, если она есть
                elif line.strip().startswith('# DATABASE_URL=postgresql:'):
                    f.write(line.replace('# DATABASE_URL', 'DATABASE_URL'))
                else:
                    f.write(line)
        
        print("✅ Конфигурация переключена на PostgreSQL")
        print(f"✅ DATABASE_URL установлен: postgresql://{db_user}:****@{db_host}:{db_port}/{db_name}")
        print("\nТеперь выполните следующие команды для инициализации базы данных:")
        print("1. python -m app.migrations_update")
        print("2. python -m app.run")
        print("\nЕсли вы хотите вернуться к SQLite, запустите скрипт switch_to_sqlite.py")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("=== Переключение на PostgreSQL для продакшена ===")
    
    if input("Вы уверены, что хотите переключиться на PostgreSQL? (y/n): ").lower() == 'y':
        switch_to_postgres()
    else:
        print("Операция отменена.")
