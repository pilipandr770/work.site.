#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для обновления адреса токен-контракта в базе данных.
Используйте этот скрипт для подключения существующего токена или после деплоя нового контракта.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app, db
from app.models import Token

# Загружаем переменные окружения
load_dotenv()

def update_token_address(contract_address, token_name=None, token_symbol=None):
    """
    Обновляет адрес токен-контракта в базе данных
    
    Args:
        contract_address (str): Адрес токен-контракта
        token_name (str, optional): Название токена
        token_symbol (str, optional): Символ токена
    """
    app = create_app()
    
    with app.app_context():
        # Ищем существующий токен
        token = Token.query.first()
        
        if not token:
            # Создаем новый токен, если его нет
            token = Token(
                name=token_name or "IT Shop Token",
                symbol=token_symbol or "ITST",
                contract_address=contract_address,
                decimals=18,
                total_supply=1000000,  # 1M токенов
                circulating_supply=700000,  # 70% в обращении
                token_price_usd=0.1,  # $0.1 за токен
                description="Токен экосистемы IT Shop для оплаты товаров, участия в DAO и получения вознаграждений.",
                description_ua="Токен екосистеми IT Shop для оплати товарів, участі в DAO та отримання винагород.",
                description_en="IT Shop ecosystem token for paying goods, participating in DAO and earning rewards.",
                description_de="IT Shop Ökosystem-Token für die Bezahlung von Waren, die Teilnahme an DAO und das Verdienen von Belohnungen.",
                description_ru="Токен экосистемы IT Shop для оплаты товаров, участия в DAO и получения вознаграждений."
            )
            db.session.add(token)
            print(f"✅ Создан новый токен: {token.name} ({token.symbol})")
        else:
            # Обновляем существующий токен
            token.contract_address = contract_address
            if token_name:
                token.name = token_name
            if token_symbol:
                token.symbol = token_symbol
            print(f"✅ Обновлен существующий токен: {token.name} ({token.symbol})")
        
        # Сохраняем изменения
        db.session.commit()
        
        print(f"📝 Адрес контракта обновлен: {contract_address}")
        print(f"🌐 Просмотр в Polygonscan: https://polygonscan.com/token/{contract_address}")
        print(f"🧪 Просмотр в Mumbai Testnet: https://mumbai.polygonscan.com/token/{contract_address}")

def main():
    """Основная функция"""
    print("🔧 Обновление адреса токен-контракта")
    print("=" * 50)
    
    # Получаем адрес контракта из переменных окружения или от пользователя
    contract_address = os.getenv('EXISTING_TOKEN_ADDRESS') or os.getenv('CONTRACT_ADDRESS')
    
    if not contract_address or contract_address == "0x1234567890123456789012345678901234567890":
        print("⚠️  Адрес контракта не найден в .env файле.")
        print("\nВарианты:")
        print("1. Использовать существующий токен на Polygon")
        print("2. Задеплоить новый контракт")
        print("3. Ввести адрес контракта вручную")
        
        choice = input("\nВыберите вариант (1/2/3): ").strip()
        
        if choice == "1":
            contract_address = input("Введите адрес вашего существующего токена: ").strip()
            token_name = input("Введите название токена (или Enter для 'IT Shop Token'): ").strip() or None
            token_symbol = input("Введите символ токена (или Enter для 'ITST'): ").strip() or None
            
        elif choice == "2":
            print("🚀 Запуск деплоя нового контракта...")
            print("Выполните команду: python deploy_contracts.py")
            print("После деплоя запустите этот скрипт снова.")
            return
            
        elif choice == "3":
            contract_address = input("Введите адрес контракта: ").strip()
            token_name = input("Введите название токена (или Enter для пропуска): ").strip() or None
            token_symbol = input("Введите символ токена (или Enter для пропуска): ").strip() or None
        
        else:
            print("❌ Неверный выбор")
            return
    else:
        token_name = None
        token_symbol = None
        print(f"📋 Найден адрес контракта в .env: {contract_address}")
    
    # Валидация адреса
    if not contract_address or len(contract_address) != 42 or not contract_address.startswith('0x'):
        print("❌ Неверный формат адреса контракта. Должен быть 42 символа, начинающийся с '0x'")
        return
    
    # Обновляем токен
    try:
        update_token_address(contract_address, token_name, token_symbol)
        print("\n✅ Токен успешно обновлен!")
        print("🌟 Теперь вы можете использовать все блокчейн функции сайта.")
        
        # Обновляем .env файл
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Обновляем CONTRACT_ADDRESS
            if 'CONTRACT_ADDRESS=' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if line.startswith('CONTRACT_ADDRESS='):
                        lines[i] = f'CONTRACT_ADDRESS={contract_address}'
                        break
                
                with open(env_path, 'w', encoding='utf-8') as file:
                    file.write('\n'.join(lines))
                
                print(f"📝 Файл .env обновлен с новым адресом контракта.")
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении токена: {e}")

if __name__ == "__main__":
    main()
