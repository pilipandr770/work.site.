#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для настройки блокчейн-интеграции IT Shop.
Помогает настроить все необходимые параметры для работы с токен-контрактом.
"""

import os
import sys
from pathlib import Path

def setup_blockchain_config():
    """Настройка блокчейн-конфигурации"""
    print("🔧 Настройка блокчейн-интеграции IT Shop")
    print("=" * 50)
    
    env_path = Path('.env')
    
    # Читаем существующий .env файл
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as file:
            content = file.read()
    else:
        content = ""
    
    print("Выберите способ интеграции с блокчейном:")
    print("1. 🔗 Использовать существующий токен на Polygon")
    print("2. 🚀 Создать новый токен-контракт")
    print("3. 🧪 Настроить для тестирования (Mumbai Testnet)")
    
    choice = input("\nВыберите вариант (1/2/3): ").strip()
    
    if choice == "1":
        setup_existing_token(content, env_path)
    elif choice == "2":
        setup_new_contract(content, env_path)
    elif choice == "3":
        setup_testnet(content, env_path)
    else:
        print("❌ Неверный выбор")
        return
    
    print("\n✅ Настройка завершена!")
    print("📋 Следующие шаги:")
    print("- Проверьте файл .env")
    print("- Запустите: python update_token_address.py")
    print("- Протестируйте функционал на сайте")

def setup_existing_token(content, env_path):
    """Настройка существующего токена"""
    print("\n🔗 Настройка существующего токена")
    print("-" * 30)
    
    token_address = input("Введите адрес вашего токена: ").strip()
    if not validate_address(token_address):
        print("❌ Неверный формат адреса")
        return
    
    network = input("Сеть (mainnet/mumbai) [mainnet]: ").strip().lower() or "mainnet"
    
    # Обновляем конфигурацию
    config_updates = {
        'CONTRACT_ADDRESS': token_address,
        'EXISTING_TOKEN_ADDRESS': token_address,
        'POLYGON_NETWORK': network,
    }
    
    updated_content = update_env_content(content, config_updates)
    
    with open(env_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print(f"✅ Токен настроен: {token_address}")
    print(f"🌐 Сеть: {network}")

def setup_new_contract(content, env_path):
    """Настройка нового контракта"""
    print("\n🚀 Настройка нового контракта")
    print("-" * 30)
    
    print("Для деплоя нового контракта необходимо:")
    print("1. INFURA_API_KEY - получите на https://infura.io/")
    print("2. POLYGON_PRIVATE_KEY - экспортируйте из MetaMask")
    print("3. MATIC на кошельке для оплаты газа")
    
    infura_key = input("\nВведите INFURA_API_KEY: ").strip()
    if not infura_key:
        print("❌ INFURA_API_KEY обязателен")
        return
    
    private_key = input("Введите приватный ключ (начинается с 0x): ").strip()
    if not private_key or len(private_key) != 66:
        print("❌ Неверный формат приватного ключа")
        return
    
    network = input("Сеть для деплоя (mainnet/mumbai) [mumbai]: ").strip().lower() or "mumbai"
    
    # Обновляем конфигурацию
    config_updates = {
        'INFURA_API_KEY': infura_key,
        'POLYGON_PRIVATE_KEY': private_key,
        'POLYGON_NETWORK': network,
        'DEPLOY_NEW_CONTRACT': 'true',
    }
    
    updated_content = update_env_content(content, config_updates)
    
    with open(env_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print(f"✅ Конфигурация для деплоя настроена")
    print(f"🌐 Сеть: {network}")
    print("\n🚀 Для деплоя выполните: python deploy_contracts.py")

def setup_testnet(content, env_path):
    """Настройка тестовой сети"""
    print("\n🧪 Настройка Mumbai Testnet")
    print("-" * 30)
    
    print("Настройка тестовой конфигурации:")
    print("- Сеть: Polygon Mumbai Testnet")
    print("- Тестовый токен: будет использован placeholder")
    print("- Функции работают в demo-режиме")
    
    # Обновляем конфигурацию
    config_updates = {
        'POLYGON_NETWORK': 'mumbai',
        'CONTRACT_ADDRESS': '0x1234567890123456789012345678901234567890',
        'TESTNET_MODE': 'true',
    }
    
    updated_content = update_env_content(content, config_updates)
    
    with open(env_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)
    
    print("✅ Тестовая конфигурация настроена")
    print("💡 Для получения тестовых MATIC: https://faucet.polygon.technology/")

def update_env_content(content, updates):
    """Обновляет содержимое .env файла"""
    lines = content.split('\n') if content else []
    
    # Создаем словарь существующих переменных
    existing_vars = {}
    for i, line in enumerate(lines):
        if '=' in line and not line.strip().startswith('#'):
            key = line.split('=')[0].strip()
            existing_vars[key] = i
    
    # Обновляем существующие или добавляем новые переменные
    for key, value in updates.items():
        if key in existing_vars:
            lines[existing_vars[key]] = f"{key}={value}"
        else:
            lines.append(f"{key}={value}")
    
    # Удаляем пустые строки в конце
    while lines and not lines[-1].strip():
        lines.pop()
    
    return '\n'.join(lines)

def validate_address(address):
    """Валидация Ethereum адреса"""
    return (
        address and 
        len(address) == 42 and 
        address.startswith('0x') and 
        all(c in '0123456789abcdefABCDEF' for c in address[2:])
    )

def main():
    """Основная функция"""
    try:
        setup_blockchain_config()
    except KeyboardInterrupt:
        print("\n❌ Настройка прервана пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    main()
