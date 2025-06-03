#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для проверки состояния блокчейн-интеграции IT Shop.
Выполняет диагностику всех компонентов и дает рекомендации.
"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv

# Добавляем корневую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

# Загружаем переменные окружения
load_dotenv()

def check_environment():
    """Проверка переменных окружения"""
    print("🔍 Проверка переменных окружения")
    print("-" * 40)
    
    required_vars = {
        'CONTRACT_ADDRESS': 'Адрес токен-контракта',
        'POLYGON_NETWORK': 'Выбранная сеть (mainnet/mumbai)',
    }
    
    optional_vars = {
        'POLYGON_PRIVATE_KEY': 'Приватный ключ для деплоя',
        'INFURA_API_KEY': 'API ключ Infura',
        'EXISTING_TOKEN_ADDRESS': 'Адрес существующего токена',
    }
    
    status = True
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value and value != "0x1234567890123456789012345678901234567890":
            print(f"✅ {var}: {description}")
        else:
            print(f"❌ {var}: НЕ НАСТРОЕН - {description}")
            status = False
    
    print("\nДополнительные переменные:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✅ {var}: {description}")
        else:
            print(f"⚪ {var}: не настроен - {description}")
    
    return status

def check_database():
    """Проверка базы данных"""
    print("\n🗄️ Проверка базы данных")
    print("-" * 40)
    
    try:
        from app import create_app, db
        from app.models import Token, Airdrop, TokenSale, DaoProposal
        
        app = create_app()
        with app.app_context():
            # Проверяем наличие токена
            token = Token.query.first()
            if token:
                print(f"✅ Токен найден: {token.name} ({token.symbol})")
                print(f"   Адрес контракта: {token.contract_address}")
                print(f"   Общее предложение: {token.total_supply}")
                
                # Проверяем соответствие адреса в .env и БД
                env_address = os.getenv('CONTRACT_ADDRESS')
                if token.contract_address == env_address:
                    print("✅ Адрес контракта в БД соответствует .env")
                else:
                    print("⚠️  Адрес контракта в БД не соответствует .env")
                    print(f"   БД: {token.contract_address}")
                    print(f"   .env: {env_address}")
            else:
                print("❌ Токен не найден в базе данных")
                return False
            
            # Проверяем наличие демо-данных
            airdrop_count = Airdrop.query.count()
            tokensale_count = TokenSale.query.count()
            dao_count = DaoProposal.query.count()
            
            print(f"📊 Демо-данные:")
            print(f"   Аирдропы: {airdrop_count}")
            print(f"   Токенсейлы: {tokensale_count}")
            print(f"   DAO предложения: {dao_count}")
            
            if airdrop_count == 0 and tokensale_count == 0 and dao_count == 0:
                print("💡 Рекомендация: запустите python utils/demo_data.py")
            
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки БД: {e}")
        return False

def check_contract_files():
    """Проверка файлов контракта"""
    print("\n📄 Проверка файлов контракта")
    print("-" * 40)
    
    contract_file = Path("contracts/ITShopToken.sol")
    deploy_script = Path("deploy_contracts.py")
    deployments_dir = Path("deployments")
    
    status = True
    
    if contract_file.exists():
        print("✅ Файл контракта ITShopToken.sol найден")
    else:
        print("❌ Файл контракта ITShopToken.sol не найден")
        status = False
    
    if deploy_script.exists():
        print("✅ Скрипт деплоя deploy_contracts.py найден")
    else:
        print("❌ Скрипт деплоя deploy_contracts.py не найден")
        status = False
    
    if deployments_dir.exists():
        contract_data_file = deployments_dir / "contract_data.json"
        if contract_data_file.exists():
            try:
                with open(contract_data_file, 'r') as f:
                    data = json.load(f)
                print("✅ Данные деплоя найдены")
                print(f"   Адрес: {data.get('token_address', 'N/A')}")
                print(f"   Сеть: {data.get('network', 'N/A')}")
                print(f"   Дата деплоя: {data.get('deploy_date', 'N/A')}")
            except Exception as e:
                print(f"⚠️  Ошибка чтения данных деплоя: {e}")
        else:
            print("⚪ Данные деплоя не найдены (contract_data.json)")
    else:
        print("⚪ Директория deployments не найдена")
    
    return status

def check_web3_integration():
    """Проверка Web3 интеграции"""
    print("\n🌐 Проверка Web3 интеграции")
    print("-" * 40)
    
    js_files = {
        'static/js/web3_utils.js': 'Утилиты Web3',
        'static/js/blockchain.js': 'Блокчейн функции',
    }
    
    css_files = {
        'static/css/blockchain.css': 'Стили блокчейн компонентов',
    }
    
    template_dirs = {
        'templates/blockchain/': 'Шаблоны блокчейн страниц',
    }
    
    status = True
    
    print("JavaScript файлы:")
    for file_path, description in js_files.items():
        if Path(file_path).exists():
            print(f"✅ {file_path}: {description}")
        else:
            print(f"❌ {file_path}: НЕ НАЙДЕН - {description}")
            status = False
    
    print("\nCSS файлы:")
    for file_path, description in css_files.items():
        if Path(file_path).exists():
            print(f"✅ {file_path}: {description}")
        else:
            print(f"❌ {file_path}: НЕ НАЙДЕН - {description}")
            status = False
    
    print("\nШаблоны:")
    for dir_path, description in template_dirs.items():
        if Path(dir_path).exists():
            template_count = len(list(Path(dir_path).glob('*.html')))
            print(f"✅ {dir_path}: {description} ({template_count} файлов)")
        else:
            print(f"❌ {dir_path}: НЕ НАЙДЕН - {description}")
            status = False
    
    return status

def check_routes():
    """Проверка маршрутов"""
    print("\n🛣️ Проверка маршрутов")
    print("-" * 40)
    
    try:
        from app import create_app
        app = create_app()
        
        blockchain_routes = []
        for rule in app.url_map.iter_rules():
            if 'blockchain' in rule.rule:
                blockchain_routes.append(rule.rule)
        
        if blockchain_routes:
            print(f"✅ Найдено {len(blockchain_routes)} блокчейн маршрутов:")
            for route in sorted(blockchain_routes):
                print(f"   {route}")
        else:
            print("❌ Блокчейн маршруты не найдены")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Ошибка проверки маршрутов: {e}")
        return False

def provide_recommendations(env_ok, db_ok, files_ok, web3_ok, routes_ok):
    """Предоставляет рекомендации по устранению проблем"""
    print("\n💡 Рекомендации")
    print("=" * 50)
    
    if not env_ok:
        print("🔧 Настройка окружения:")
        print("   python setup_blockchain.py")
    
    if not db_ok:
        print("🗄️ Настройка базы данных:")
        print("   python update_token_address.py")
        print("   python utils/demo_data.py")
    
    if not files_ok:
        print("📄 Проверьте файлы контракта:")
        print("   Убедитесь, что все файлы на месте")
    
    if not web3_ok:
        print("🌐 Проверьте Web3 интеграцию:")
        print("   Убедитесь, что JS/CSS файлы существуют")
    
    if not routes_ok:
        print("🛣️ Проверьте маршруты:")
        print("   Убедитесь, что блокчейн модуль подключен")
    
    if all([env_ok, db_ok, files_ok, web3_ok, routes_ok]):
        print("🎉 Все компоненты работают корректно!")
        print("\n📋 Доступные функции:")
        print("   • Просмотр информации о токене: /token")
        print("   • Участие в аирдропах: /airdrop")
        print("   • Покупка токенов: /token-sale")
        print("   • DAO голосование: /dao")
        print("\n🔗 Полезные ссылки:")
        
        network = os.getenv('POLYGON_NETWORK', 'mumbai')
        contract_address = os.getenv('CONTRACT_ADDRESS')
        
        if contract_address and contract_address != "0x1234567890123456789012345678901234567890":
            if network == 'mainnet':
                print(f"   • Polygonscan: https://polygonscan.com/token/{contract_address}")
            else:
                print(f"   • Mumbai Polygonscan: https://mumbai.polygonscan.com/token/{contract_address}")
        
        print("   • Добавить токен в MetaMask")
        print("   • Получить тестовые MATIC: https://faucet.polygon.technology/")

def main():
    """Основная функция диагностики"""
    print("🔍 ДИАГНОСТИКА БЛОКЧЕЙН-ИНТЕГРАЦИИ IT SHOP")
    print("=" * 60)
    
    # Выполняем все проверки
    env_ok = check_environment()
    db_ok = check_database()
    files_ok = check_contract_files()
    web3_ok = check_web3_integration()
    routes_ok = check_routes()
    
    # Предоставляем рекомендации
    provide_recommendations(env_ok, db_ok, files_ok, web3_ok, routes_ok)
    
    # Итоговый статус
    total_checks = 5
    passed_checks = sum([env_ok, db_ok, files_ok, web3_ok, routes_ok])
    
    print(f"\n📊 ИТОГО: {passed_checks}/{total_checks} проверок пройдено")
    
    if passed_checks == total_checks:
        print("✅ Блокчейн-интеграция полностью готова!")
        return 0
    elif passed_checks >= 3:
        print("⚠️  Блокчейн-интеграция частично готова")
        return 1
    else:
        print("❌ Блокчейн-интеграция требует настройки")
        return 2

if __name__ == "__main__":
    sys.exit(main())
