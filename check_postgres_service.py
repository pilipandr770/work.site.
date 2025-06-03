"""
Скрипт для проверки запущенных служб PostgreSQL и доступных портов.
"""
import os
import subprocess
import socket

def check_postgresql_service():
    try:
        print("Проверяем службы PostgreSQL...")
        result = subprocess.run(
            ['sc', 'query', 'postgresql*'], 
            capture_output=True, 
            text=True, 
            check=False
        )
        print(result.stdout)
        
        if "RUNNING" in result.stdout:
            print("✅ Служба PostgreSQL запущена")
        else:
            print("❌ Служба PostgreSQL, возможно, не запущена")
            
    except Exception as e:
        print(f"❌ Ошибка при проверке службы: {e}")

def check_postgresql_processes():
    try:
        print("\nПроверяем процессы PostgreSQL...")
        result = subprocess.run(
            ['tasklist', '/fi', 'imagename eq postgres*'], 
            capture_output=True, 
            text=True,
            check=False
        )
        print(result.stdout)
        
        if "postgres" in result.stdout.lower():
            print("✅ Процессы PostgreSQL обнаружены")
        else:
            print("❌ Процессы PostgreSQL не обнаружены")
    except Exception as e:
        print(f"❌ Ошибка при проверке процессов: {e}")

def check_open_ports():
    print("\nПроверяем открытые порты...")
    common_ports = [5432, 5433, 5434]
    
    for port in common_ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('localhost', port))
        if result == 0:
            print(f"✅ Порт {port} открыт - возможно, PostgreSQL работает на нем")
        else:
            print(f"❌ Порт {port} закрыт")
        sock.close()

if __name__ == "__main__":
    print("=== Диагностика PostgreSQL ===\n")
    
    check_postgresql_service()
    check_postgresql_processes()
    check_open_ports()
    
    print("\n=== Рекомендации ===")
    print("1. Убедитесь, что PostgreSQL установлен и запущен")
    print("2. Проверьте правильность имени пользователя и пароля")
    print("3. Проверьте порт, на котором работает PostgreSQL (обычно 5432)")
    print("4. Проверьте настройки pg_hba.conf для разрешения подключений")
    print("5. Проверьте наличие брандмауэра или антивируса, блокирующего подключения")
