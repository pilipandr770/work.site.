"""
Скрипт для переключения проекта с PostgreSQL на SQLite для тестирования.
"""
import os
import sys

def switch_to_sqlite():
    """Переключает конфигурацию на SQLite для тестирования"""
    try:
        # Создаем бэкап текущего .env файла
        with open('.env', 'r') as f:
            env_content = f.read()
        
        with open('.env.backup', 'w') as f:
            f.write(env_content)
            print("✅ Создан бэкап файла .env как .env.backup")
        
        # Обновляем .env для использования SQLite
        with open('.env', 'r') as f:
            lines = f.readlines()
        
        with open('.env', 'w') as f:
            for line in lines:
                # Закомментируем строку с PostgreSQL
                if line.strip().startswith('DATABASE_URL=postgresql://'):
                    f.write('# ' + line)
                # Раскомментируем строку с SQLite
                elif line.strip().startswith('# DATABASE_URL=sqlite:///'):
                    f.write(line.replace('# DATABASE_URL', 'DATABASE_URL'))
                else:
                    f.write(line)
        
        print("✅ Конфигурация переключена на SQLite")
        print("✅ Готово! Теперь запустите приложение для проверки с SQLite")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    print("=== Переключение на SQLite для тестирования ===")
    
    if input("Вы уверены, что хотите переключиться на SQLite? (y/n): ").lower() == 'y':
        switch_to_sqlite()
    else:
        print("Операция отменена.")
