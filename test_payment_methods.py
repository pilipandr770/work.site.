#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Тестирование функциональности добавления платежных методов в админке
"""

from app import create_app, db
from app.models import PaymentMethod, User
import json

app = create_app()

def test_payment_methods():
    """Тестирование создания платежных методов"""
    
    with app.app_context():
        print("🔍 Проверка существующих платежных методов...")
        existing_methods = PaymentMethod.query.all()
        print(f"Найдено методов: {len(existing_methods)}")
        
        for method in existing_methods:
            print(f"- {method.name} ({method.type}) - Активен: {method.is_active}")
            if method.details:
                print(f"  Детали: {method.details}")
        
        print("\n➕ Создание тестовых платежных методов...")
        
        # 1. Stripe метод с URL
        stripe_details = {
            "url": "https://buy.stripe.com/test_payment_link",
            "description": "Безопасная оплата банковской картой"
        }
        
        stripe_method = PaymentMethod(
            name="Stripe Payment",
            name_ua="Оплата картою",
            name_en="Card Payment", 
            name_de="Kartenzahlung",
            name_ru="Оплата картой",
            type="stripe",
            details=stripe_details,
            description_ua="Оплата банківською картою через Stripe",
            description_en="Bank card payment via Stripe",
            description_de="Bankkartenzahlung über Stripe", 
            description_ru="Оплата банковской картой через Stripe",
            is_active=True,
            order=1
        )
        
        # 2. PayPal метод
        paypal_details = {
            "url": "https://paypal.me/yourstore/amount",
            "email": "payments@yourstore.com"
        }
        
        paypal_method = PaymentMethod(
            name="PayPal",
            name_ua="PayPal",
            name_en="PayPal",
            name_de="PayPal", 
            name_ru="PayPal",
            type="paypal",
            details=paypal_details,
            description_ua="Оплата через PayPal",
            description_en="Payment via PayPal",
            description_de="Zahlung über PayPal",
            description_ru="Оплата через PayPal", 
            is_active=True,
            order=2
        )
        
        # 3. Bitcoin метод
        btc_details = {
            "address": "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh",
            "network": "Bitcoin Mainnet"
        }
        
        btc_method = PaymentMethod(
            name="Bitcoin",
            name_ua="Біткоїн", 
            name_en="Bitcoin",
            name_de="Bitcoin",
            name_ru="Биткоин",
            type="btc",
            details=btc_details,
            description_ua="Оплата біткоїнами",
            description_en="Bitcoin payment",
            description_de="Bitcoin-Zahlung",
            description_ru="Оплата биткоинами",
            is_active=True,
            order=3
        )
        
        # 4. Банковский перевод
        bank_details = {
            "iban": "DE89 3704 0044 0532 0130 00",
            "bic": "COBADEFFXXX",
            "recipient": "Your Company Ltd",
            "bank": "Commerzbank AG"
        }
        
        bank_method = PaymentMethod(
            name="Bank Transfer",
            name_ua="Банківський переказ",
            name_en="Bank Transfer", 
            name_de="Banküberweisung",
            name_ru="Банковский перевод",
            type="bank",
            details=bank_details,
            description_ua="Переказ на банківський рахунок",
            description_en="Transfer to bank account",
            description_de="Überweisung auf Bankkonto",
            description_ru="Перевод на банковский счет",
            is_active=True,
            order=4
        )
        
        # Добавляем методы только если их еще нет
        methods_to_add = [stripe_method, paypal_method, btc_method, bank_method]
        
        for method in methods_to_add:
            existing = PaymentMethod.query.filter_by(type=method.type).first()
            if not existing:
                db.session.add(method)
                print(f"✅ Добавлен метод: {method.name}")
            else:
                print(f"⚠️  Метод {method.type} уже существует")
        
        db.session.commit()
        print("\n✨ Тестовые данные созданы!")
        
        # Проверка URL в деталях
        print("\n🔗 Проверка URL в деталях методов:")
        all_methods = PaymentMethod.query.all()
        for method in all_methods:
            if method.details and isinstance(method.details, dict):
                if 'url' in method.details:
                    print(f"- {method.name}: URL = {method.details['url']}")
                else:
                    print(f"- {method.name}: URL не найден в деталях")
            else:
                print(f"- {method.name}: Детали отсутствуют или не JSON")

def check_admin_user():
    """Проверка админ пользователя"""
    with app.app_context():
        user = User.query.filter_by(username='andrii770').first()
        if user:
            print(f"✅ Админ пользователь найден: {user.username}")
            from werkzeug.security import check_password_hash
            is_valid = check_password_hash(user.password_hash, 'Dnepr75ok10')
            print(f"✅ Пароль корректен: {is_valid}")
        else:
            print("❌ Админ пользователь не найден")

if __name__ == "__main__":
    print("🚀 Запуск тестирования платежных методов...")
    check_admin_user()
    test_payment_methods()
    print("🎉 Тестирование завершено!")
