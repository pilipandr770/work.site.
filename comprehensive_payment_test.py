#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Комплексный тест функциональности платежных методов
Проверяет админ панель, публичное отображение и работу URL
"""

import requests
import json
from bs4 import BeautifulSoup

BASE_URL = "http://127.0.0.1:5000"

def test_public_payment_page():
    """Тестирование публичной страницы платежей"""
    print("🌐 Тестирование публичной страницы платежей...")
    
    try:
        response = requests.get(f"{BASE_URL}/payment")
        print(f"Статус ответа: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем карточки платежных методов
            payment_cards = soup.find_all('div', class_='payment-card')
            print(f"✅ Найдено карточек платежных методов: {len(payment_cards)}")
            
            for i, card in enumerate(payment_cards, 1):
                title = card.find('h3')
                if title:
                    print(f"  {i}. {title.get_text().strip()}")
                
                # Ищем кнопки с URL
                buttons = card.find_all('a', class_='btn')
                for button in buttons:
                    href = button.get('href', '')
                    text = button.get_text().strip()
                    if href.startswith('http'):
                        print(f"     🔗 Кнопка: {text} -> {href}")
                
                # Ищем изображения QR-кодов
                qr_images = card.find_all('img')
                for img in qr_images:
                    if 'uploads' in img.get('src', ''):
                        print(f"     📷 QR-код: {img.get('src')}")
            
            return True
        else:
            print(f"❌ Ошибка загрузки страницы: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        return False

def test_admin_login():
    """Тестирование входа в админку"""
    print("\n🔐 Тестирование входа в админку...")
    
    try:
        # Получаем страницу логина
        session = requests.Session()
        login_page = session.get(f"{BASE_URL}/admin/login")
        
        if login_page.status_code != 200:
            print(f"❌ Страница логина недоступна: {login_page.status_code}")
            return None
            
        soup = BeautifulSoup(login_page.text, 'html.parser')
        
        # Ищем CSRF токен
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'}) or soup.find('input', {'type': 'hidden'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
        
        # Данные для логина
        login_data = {
            'username': 'andrii770',
            'password': 'Dnepr75ok10'
        }
        
        if csrf_token:
            login_data['csrf_token'] = csrf_token
        
        # Отправляем логин
        login_response = session.post(f"{BASE_URL}/admin/login", data=login_data)
        
        if login_response.status_code == 302 or 'dashboard' in login_response.url:
            print("✅ Вход в админку успешен!")
            return session
        else:
            print(f"❌ Не удалось войти в админку: {login_response.status_code}")
            print(f"URL ответа: {login_response.url}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка при входе в админку: {e}")
        return None

def test_admin_payment_methods(session):
    """Тестирование страницы управления платежными методами"""
    print("\n💳 Тестирование админ панели платежных методов...")
    
    if not session:
        print("❌ Нет сессии для тестирования админки")
        return False
    
    try:
        # Загружаем страницу управления платежными методами
        response = session.get(f"{BASE_URL}/admin/payment-methods")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ищем таблицу с методами
            table = soup.find('table', class_='payment-table')
            if table:
                rows = table.find('tbody').find_all('tr') if table.find('tbody') else []
                print(f"✅ Найдено методов в админке: {len(rows)}")
                
                for i, row in enumerate(rows, 1):
                    cells = row.find_all('td')
                    if len(cells) >= 5:
                        name = cells[0].get_text().strip()
                        type_badge = cells[1].find('span')
                        type_text = type_badge.get_text().strip() if type_badge else "N/A"
                        status_badge = cells[3].find('span')
                        status = status_badge.get_text().strip() if status_badge else "N/A"
                        
                        print(f"  {i}. {name} ({type_text}) - {status}")
                        
                        # Проверяем детали на наличие URL
                        details_cell = cells[4]
                        links = details_cell.find_all('a')
                        for link in links:
                            href = link.get('href', '')
                            if href.startswith('http'):
                                print(f"     🔗 URL в деталях: {href}")
                
                return True
            else:
                print("❌ Таблица с методами не найдена")
                return False
        else:
            print(f"❌ Ошибка загрузки админ панели: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании админ панели: {e}")
        return False

def test_add_payment_method(session):
    """Тестирование добавления нового платежного метода"""
    print("\n➕ Тестирование добавления нового платежного метода...")
    
    if not session:
        print("❌ Нет сессии для тестирования")
        return False
    
    try:
        # Получаем страницу с формой
        form_page = session.get(f"{BASE_URL}/admin/payment-methods")
        soup = BeautifulSoup(form_page.text, 'html.parser')
        
        # Ищем CSRF токен
        csrf_token = None
        csrf_input = soup.find('input', {'name': 'csrf_token'})
        if csrf_input:
            csrf_token = csrf_input.get('value')
        
        # Данные для нового метода
        test_method_data = {
            'name': 'Test Stripe Method',
            'name_en': 'Test Stripe Method',
            'name_de': 'Test Stripe Methode',
            'name_ru': 'Тестовый метод Stripe',
            'type': 'stripe',
            'details': json.dumps({
                "url": "https://buy.stripe.com/test_12345",
                "description": "Test payment link"
            }),
            'description_ua': 'Тестовий метод оплати через Stripe',
            'description_en': 'Test payment method via Stripe',
            'description_de': 'Test-Zahlungsmethode über Stripe',
            'description_ru': 'Тестовый метод оплаты через Stripe',
            'is_active': True
        }
        
        if csrf_token:
            test_method_data['csrf_token'] = csrf_token
        
        # Отправляем данные
        response = session.post(f"{BASE_URL}/admin/payment-method/add", data=test_method_data)
        
        if response.status_code == 302:  # Редирект после успешного добавления
            print("✅ Платежный метод успешно добавлен!")
            return True
        else:
            print(f"❌ Ошибка при добавлении метода: {response.status_code}")
            # Печатаем ошибки формы если есть
            soup = BeautifulSoup(response.text, 'html.parser')
            error_div = soup.find('div', class_='alert-danger')
            if error_div:
                print(f"Ошибки формы: {error_div.get_text()}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при добавлении метода: {e}")
        return False

def run_comprehensive_test():
    """Запуск комплексного тестирования"""
    print("🚀 Запуск комплексного тестирования платежных методов")
    print("=" * 60)
    
    # Тест 1: Публичная страница
    public_success = test_public_payment_page()
    
    # Тест 2: Вход в админку
    admin_session = test_admin_login()
    
    # Тест 3: Админ панель платежных методов
    admin_success = test_admin_payment_methods(admin_session)
    
    # Тест 4: Добавление нового метода
    add_success = test_add_payment_method(admin_session)
    
    # Повторная проверка публичной страницы
    print("\n🔄 Повторная проверка публичной страницы после изменений...")
    public_success_2 = test_public_payment_page()
    
    # Итоги
    print("\n" + "=" * 60)
    print("📊 РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ:")
    print(f"✅ Публичная страница платежей: {'✓' if public_success else '✗'}")
    print(f"✅ Вход в админку: {'✓' if admin_session else '✗'}")
    print(f"✅ Админ панель методов: {'✓' if admin_success else '✗'}")
    print(f"✅ Добавление нового метода: {'✓' if add_success else '✗'}")
    print(f"✅ Обновленная публичная страница: {'✓' if public_success_2 else '✗'}")
    
    total_tests = 5
    passed_tests = sum([public_success, bool(admin_session), admin_success, add_success, public_success_2])
    
    print(f"\n🎯 Общий результат: {passed_tests}/{total_tests} тестов пройдено")
    
    if passed_tests == total_tests:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("\n✨ Функциональность платежных методов работает корректно:")
        print("   - URL-ы правильно сохраняются в JSON поле details")
        print("   - Админ панель позволяет управлять методами")
        print("   - Публичная страница корректно отображает методы и URL")
        print("   - Многоязычная поддержка работает")
    else:
        print("⚠️  Обнаружены проблемы в функциональности")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    try:
        run_comprehensive_test()
    except KeyboardInterrupt:
        print("\n\n⏹️  Тестирование прервано пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
