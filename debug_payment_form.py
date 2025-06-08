#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт для отладки формы добавления платежных методов
"""

from app import create_app, db
from app.models import PaymentMethod
from app.forms import PaymentMethodForm
import json

def test_payment_form():
    app = create_app()
    
    with app.app_context():
        print("=== ТЕСТ ФОРМЫ ПЛАТЕЖНЫХ МЕТОДОВ ===\n")
        
        # Тестируем различные форматы JSON
        test_cases = [
            {
                'name': 'Test Stripe',
                'type': 'stripe',
                'details': '{"url": "https://buy.stripe.com/test_12345"}',
                'description': 'Валидный JSON с URL'
            },
            {
                'name': 'Test PayPal',
                'type': 'paypal', 
                'details': '{"url": "https://paypal.me/test/100"}',
                'description': 'Валидный JSON с PayPal URL'
            },
            {
                'name': 'Test Invalid JSON',
                'type': 'stripe',
                'details': '{url: "https://test.com"}',  # Неправильный JSON
                'description': 'Неправильный JSON без кавычек'
            },
            {
                'name': 'Test Empty',
                'type': 'bank',
                'details': '',
                'description': 'Пустое поле details'
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"--- ТЕСТ {i}: {test_case['description']} ---")
            
            # Создаем форму и заполняем данными
            form = PaymentMethodForm()
            form.name.data = test_case['name']
            form.type.data = test_case['type']
            form.details.data = test_case['details']
            form.is_active.data = True
            
            print(f"Название: {form.name.data}")
            print(f"Тип: {form.type.data}")
            print(f"Details (RAW): {repr(form.details.data)}")
            
            # Пробуем парсить JSON как в админке
            try:
                parsed_details = json.loads(form.details.data) if form.details.data else None
                print(f"Парсинг JSON: ✅ Успех")
                print(f"Парсированные данные: {parsed_details}")
            except json.JSONDecodeError as e:
                print(f"Парсинг JSON: ❌ Ошибка - {e}")
                print(f"Будет сохранено как строка: {repr(form.details.data)}")
                parsed_details = form.details.data
            except Exception as e:
                print(f"Парсинг JSON: ❌ Другая ошибка - {e}")
                parsed_details = form.details.data
            
            print(f"Финальное значение для БД: {repr(parsed_details)}")
            print()

def check_existing_methods():
    app = create_app()
    
    with app.app_context():
        print("=== СУЩЕСТВУЮЩИЕ МЕТОДЫ В БД ===\n")
        
        methods = PaymentMethod.query.all()
        
        for method in methods:
            print(f"ID: {method.id}")
            print(f"Название: {method.name}")
            print(f"Тип: {method.type}")
            print(f"Details (тип): {type(method.details)}")
            print(f"Details (значение): {repr(method.details)}")
            
            # Проверяем, есть ли URL
            if isinstance(method.details, dict) and 'url' in method.details:
                print(f"✅ URL найден: {method.details['url']}")
            elif isinstance(method.details, str):
                try:
                    parsed = json.loads(method.details)
                    if 'url' in parsed:
                        print(f"✅ URL найден в строке: {parsed['url']}")
                    else:
                        print("❌ URL не найден")
                except:
                    print("❌ Не удалось парсить строку как JSON")
            else:
                print("❌ URL не найден")
            
            print(f"Активен: {method.is_active}")
            print("---")

if __name__ == "__main__":
    print("🔍 ОТЛАДКА ФОРМЫ ПЛАТЕЖНЫХ МЕТОДОВ\n")
    
    check_existing_methods()
    print("\n" + "="*50 + "\n")
    test_payment_form()
    
    print("\n✅ Отладка завершена")
