"""
Скрипт для проверки загрузки переменных окружения из .env файла.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Пути к возможным .env файлам
ROOT_DIR = Path(__file__).resolve().parent
ENV_PATHS = [
    ROOT_DIR / '.env',
    ROOT_DIR / 'app' / '.env',
    ROOT_DIR
]

def check_env_files():
    """Проверяем наличие .env файлов"""
    print("\nПоиск .env файлов:")
    for path in ENV_PATHS:
        env_path = path / '.env' if isinstance(path, Path) else Path(path) / '.env'
        if env_path.exists():
            print(f"✅ Найден .env файл: {env_path}")
            try:
                with open(env_path, 'r') as f:
                    content = f.read()
                print(f"Содержимое файла (первые 500 символов):")
                print("-" * 50)
                print(content[:500])
                print("-" * 50)
            except Exception as e:
                print(f"❌ Ошибка чтения файла: {e}")
        else:
            print(f"❌ Файл не найден: {env_path}")

def check_env_vars():
    """Проверяем переменные окружения"""
    print("\nПроверка переменных окружения:")
    vars_to_check = ['DATABASE_URL', 'SECRET_KEY', 'TOKEN_CONTRACT_ADDRESS']
    
    for var in vars_to_check:
        value = os.environ.get(var)
        if value:
            masked_value = value[:5] + '*****' + value[-5:] if len(value) > 15 else value[:2] + '****'
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: не найдена")

def try_load_dotenv():
    """Пытаемся загрузить переменные из .env"""
    print("\nЗагружаем переменные с помощью python-dotenv:")
    
    # Проверяем, установлен ли python-dotenv
    try:
        import dotenv
        print("✅ python-dotenv установлен")
    except ImportError:
        print("❌ python-dotenv не установлен, устанавливаем...")
        import subprocess
        subprocess.call([sys.executable, '-m', 'pip', 'install', 'python-dotenv'])
        import dotenv
    
    # Пытаемся загрузить из разных мест
    for path in ENV_PATHS:
        env_path = path / '.env' if isinstance(path, Path) else Path(path) / '.env'
        if env_path.exists():
            print(f"Загружаем из {env_path}...")
            dotenv.load_dotenv(env_path)
    
    # Проверяем после загрузки
    check_env_vars()

def test_import_config():
    """Тестируем импорт конфигурации"""
    print("\nТестируем импорт конфигурации:")
    try:
        sys.path.insert(0, str(ROOT_DIR))
        from app.config import Config
        config = Config()
        print(f"✅ Конфигурация успешно импортирована")
        print(f"✅ SQLALCHEMY_DATABASE_URI: {config.SQLALCHEMY_DATABASE_URI}")
    except Exception as e:
        print(f"❌ Ошибка импорта конфигурации: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("ПРОВЕРКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ")
    print("=" * 50)
    
    print(f"Текущая директория: {os.getcwd()}")
    check_env_files()
    check_env_vars()
    try_load_dotenv()
    test_import_config()
