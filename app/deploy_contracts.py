#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для деплоя смарт-контрактов на блокчейн Polygon.
Компилирует и развертывает смарт-контракты ERC20 токена, токенсейла и DAO.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from solcx import compile_standard, install_solc

# Загружаем переменные окружения из .env файла
load_dotenv()

# Устанавливаем версию solc
def install_solc_if_needed():
    """Устанавливаем компилятор Solidity если он не установлен"""
    print("Установка компилятора Solidity...")
    try:
        install_solc("0.8.19")
        print("Компилятор Solidity успешно установлен!")
    except Exception as e:
        print(f"Ошибка при установке компилятора: {e}")
        exit(1)

def compile_contract(contract_path, contract_name):
    """Компилирует смарт-контракт"""
    print(f"Компиляция контракта {contract_name}...")
    
    with open(contract_path, "r", encoding="utf-8") as file:
        contract_source = file.read()
    
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_name: {"content": contract_source}},
            "settings": {
                "outputSelection": {
                    "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
                }
            },
        },
        solc_version="0.8.19",
    )
    
    # Получаем ABI и байткод
    contract_data = compiled_sol["contracts"][contract_name][contract_name.split(".")[0]]
    abi = contract_data["abi"]
    bytecode = contract_data["evm"]["bytecode"]["object"]
    
    return abi, bytecode

def deploy_contract(w3, abi, bytecode, private_key, constructor_args=None):
    """Деплоит смарт-контракт в блокчейн"""
    account = w3.eth.account.from_key(private_key)
    
    # Создаем контракт
    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    
    # Получаем nonce для адреса отправителя
    nonce = w3.eth.get_transaction_count(account.address)
    
    # Создаем транзакцию деплоя контракта
    if constructor_args:
        transaction = Contract.constructor(*constructor_args).build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": account.address,
                "nonce": nonce,
            }
        )
    else:
        transaction = Contract.constructor().build_transaction(
            {
                "chainId": w3.eth.chain_id,
                "gasPrice": w3.eth.gas_price,
                "from": account.address,
                "nonce": nonce,
            }
        )
    
    # Подписываем транзакцию
    signed_transaction = w3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Отправляем транзакцию
    tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    
    print(f"Транзакция отправлена: {tx_hash.hex()}")
    
    # Ждем подтверждения транзакции
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_receipt.contractAddress

def main():
    """Основная функция деплоя контрактов"""
    print("🚀 Деплой токен-контракта IT Shop")
    print("=" * 40)
    
    # Проверяем наличие существующего контракта
    existing_address = os.getenv("EXISTING_TOKEN_ADDRESS") or os.getenv("CONTRACT_ADDRESS")
    if existing_address and existing_address != "0x1234567890123456789012345678901234567890":
        print(f"⚠️  Найден существующий адрес контракта: {existing_address}")
        choice = input("Все равно деплоить новый контракт? (y/N): ").strip().lower()
        if choice != 'y':
            print("Деплой отменен. Используйте существующий контракт.")
            print("Для обновления адреса в БД запустите: python update_token_address.py")
            return
    
    install_solc_if_needed()
    
    # Загружаем конфигурацию из .env
    PRIVATE_KEY = os.getenv("POLYGON_PRIVATE_KEY")
    INFURA_API_KEY = os.getenv("INFURA_API_KEY")
    
    if not PRIVATE_KEY or not INFURA_API_KEY:
        print("❌ Необходимо указать POLYGON_PRIVATE_KEY и INFURA_API_KEY в файле .env")
        print("\nФормат файла .env:")
        print("POLYGON_PRIVATE_KEY=ваш_приватный_ключ")
        print("INFURA_API_KEY=ваш_ключ_infura")
        print("\n💡 Получить ключи можно:")
        print("- INFURA_API_KEY: https://infura.io/")
        print("- POLYGON_PRIVATE_KEY: экспортируйте из MetaMask")
        exit(1)
      # Выбор сети
    network = os.getenv("POLYGON_NETWORK", "mumbai").lower()
    if network == "mainnet":
        rpc_url = f"https://polygon-mainnet.infura.io/v3/{INFURA_API_KEY}"
        chain_name = "Polygon Mainnet"
        explorer_url = "https://polygonscan.com"
    else:
        rpc_url = f"https://polygon-mumbai.infura.io/v3/{INFURA_API_KEY}"
        chain_name = "Polygon Mumbai Testnet"
        explorer_url = "https://mumbai.polygonscan.com"
    
    print(f"🌐 Подключение к {chain_name}...")
    
    # Настраиваем подключение к блокчейну
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        print(f"❌ Ошибка подключения к {chain_name}")
        print("Проверьте:")
        print("- Правильность INFURA_API_KEY")
        print("- Подключение к интернету")
        exit(1)
    
    print(f"✅ Успешное подключение к {chain_name}")
    
    # Проверяем баланс аккаунта
    account = w3.eth.account.from_key(PRIVATE_KEY)
    balance = w3.eth.get_balance(account.address)
    balance_matic = w3.from_wei(balance, 'ether')
    
    print(f"👛 Адрес кошелька: {account.address}")
    print(f"💰 Баланс: {balance_matic:.4f} MATIC")
    
    if balance_matic < 0.01:
        print("⚠️  Низкий баланс MATIC для оплаты газа!")
        if network == "mumbai":
            print("💡 Получите тестовые MATIC: https://faucet.polygon.technology/")
        else:
            print("💡 Пополните баланс MATIC на кошельке")
        
        choice = input("Продолжить деплой? (y/N): ").strip().lower()
        if choice != 'y':
            exit(1)
    
    # Пути к контрактам
    contracts_dir = Path("contracts")
    token_contract_path = contracts_dir / "ITShopToken.sol"
    
    if not token_contract_path.exists():
        print(f"Файл контракта {token_contract_path} не найден")
        exit(1)
    
    # Компилируем и деплоим токен
    token_abi, token_bytecode = compile_contract(token_contract_path, "ITShopToken.sol")
    
    # Аргументы конструктора токена: название, символ, общее предложение
    token_args = ["IT Shop Token", "ITST", 1000000 * 10**18]  # 1,000,000 токенов с 18 десятичными знаками
      # Деплоим токен
    print("\n🔨 Деплой токена...")
    token_address = deploy_contract(w3, token_abi, token_bytecode, PRIVATE_KEY, token_args)
    print(f"✅ Токен задеплоен по адресу: {token_address}")
    print(f"🔗 Просмотр в Explorer: {explorer_url}/token/{token_address}")
    
    # Сохраняем адрес и ABI контракта
    contract_data = {
        "token_address": token_address,
        "token_abi": token_abi,
        "network": network,
        "chain_name": chain_name,
        "deploy_date": str(datetime.now()),
        "deployer_address": account.address
    }
    
    # Создаем директорию для сохранения данных контрактов, если она не существует
    deploy_dir = Path("deployments")
    deploy_dir.mkdir(exist_ok=True)
      with open(deploy_dir / "contract_data.json", "w") as file:
        json.dump(contract_data, file, indent=4)
    
    print(f"💾 Данные контракта сохранены в deployments/contract_data.json")
    
    # Обновляем .env файл с адресом контракта
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, "r", encoding='utf-8') as file:
            env_content = file.read()
        
        # Обновляем CONTRACT_ADDRESS
        if "CONTRACT_ADDRESS=" in env_content:
            lines = env_content.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('CONTRACT_ADDRESS='):
                    lines[i] = f'CONTRACT_ADDRESS={token_address}'
                    break
            env_content = '\n'.join(lines)
        else:
            # Добавляем новую переменную
            env_content += f"\nCONTRACT_ADDRESS={token_address}\n"
            
        with open(env_path, "w", encoding='utf-8') as file:
            file.write(env_content)
    else:
        # Создаем новый .env файл
        with open(env_path, "w", encoding='utf-8') as file:
            file.write(f"CONTRACT_ADDRESS={token_address}\n")
    
    print("✅ Адрес контракта добавлен в .env файл")
    
    # Автоматически обновляем БД
    print("\n📝 Обновление базы данных...")
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "update_token_address.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ База данных успешно обновлена!")
        else:
            print(f"⚠️  Ошибка обновления БД: {result.stderr}")
            print("Выполните вручную: python update_token_address.py")
    except Exception as e:
        print(f"⚠️  Не удалось автоматически обновить БД: {e}")
        print("Выполните вручную: python update_token_address.py")
    
    print("\n" + "="*50)
    print("🎉 ДЕПЛОЙ УСПЕШНО ЗАВЕРШЕН!")
    print("="*50)
    print(f"📋 Адрес контракта: {token_address}")
    print(f"🌐 Сеть: {chain_name}")
    print(f"🔗 Explorer: {explorer_url}/token/{token_address}")
    print(f"👛 Владелец: {account.address}")
    print("\n💡 Следующие шаги:")
    print("1. Сохраните адрес контракта в безопасном месте")
    print("2. Добавьте токен в MetaMask для просмотра баланса")
    print("3. Протестируйте функции на сайте")
    print("4. При необходимости настройте дополнительные параметры")

if __name__ == "__main__":
    main()
