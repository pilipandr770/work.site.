#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Простой тест добавления платежного метода с URL
"""

from app import create_app, db
from app.models import PaymentMethod
import json

def test_manual_payment_creation():
    app = create_app()
    
    with app.app_context():
        print("=== ТЕСТ РУЧНОГО СОЗДАНИЯ МЕТОДА С URL ===\n")
        
        # Создаем метод точно так же, как в админке
        method = PaymentMethod()
        method.name = "Test Stripe Manual"
        method.name_ua = "Test Stripe Manual"
        method.type = "stripe"
        
        # Тестируем парсинг JSON как в админке
        json_string = '{"url": "https://buy.stripe.com/test_manual_12345"}'
        print(f"JSON строка: {json_string}")
        
        try:
            parsed_details = json.loads(json_string)
            print(f"✅ JSON парсинг успешен: {parsed_details}")
            method.details = parsed_details
        except Exception as e:
            print(f"❌ Ошибка парсинга: {e}")
            method.details = json_string
        
        method.is_active = True
        
        # Сохраняем в БД
        try:
            db.session.add(method)
            db.session.commit()
            print(f"✅ Метод сохранен с ID: {method.id}")
        except Exception as e:
            print(f"❌ Ошибка сохранения: {e}")
            db.session.rollback()
        
        print()

def check_all_methods():
    app = create_app()
    
    with app.app_context():
        print("=== ВСЕ МЕТОДЫ В БД ===\n")
        
        methods = PaymentMethod.query.all()
        
        for method in methods:
            print(f"ID: {method.id} | {method.name} ({method.type})")
            print(f"Details: {repr(method.details)}")
            
            # Проверяем URL
            if isinstance(method.details, dict) and 'url' in method.details:
                print(f"✅ URL: {method.details['url']}")
            else:
                print("❌ URL не найден")
            print("---")

def test_json_formats():
    print("=== ТЕСТ РАЗЛИЧНЫХ JSON ФОРМАТОВ ===\n")
    
    test_strings = [
        '{"url": "https://example.com"}',  # Правильный
        "{'url': 'https://example.com'}",  # Неправильный - одинарные кавычки
        '{url: "https://example.com"}',    # Неправильный - ключ без кавычек
        '{"url":"https://example.com","description":"Test"}',  # Сложный правильный
        '{"url": "https://example.com",}',  # С лишней запятой
    ]
    
    for i, test_str in enumerate(test_strings, 1):
        print(f"Тест {i}: {test_str}")
        try:
            result = json.loads(test_str)
            print(f"✅ Успех: {result}")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
        print()

if __name__ == "__main__":
    print("🔍 ТЕСТ ПЛАТЕЖНЫХ МЕТОДОВ\n")
    
    test_json_formats()
    print("\n" + "="*50 + "\n")
    check_all_methods()
    print("\n" + "="*50 + "\n")
    test_manual_payment_creation()
    print("\n" + "="*50 + "\n")
    check_all_methods()
