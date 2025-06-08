#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для создания демонстрационных данных для продуктов и категорий
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import Category, Product, ProductImage

def create_demo_products():
    """Создать демонстрационные продукты и категории"""
    app = create_app()
    
    with app.app_context():
        # Создаем категории
        categories_data = [
            {
                'name': 'Telegram боты',
                'name_en': 'Telegram Bots',
                'name_de': 'Telegram Bots',
                'name_ru': 'Telegram боты',
                'slug': 'telegram-bots',
                'description': 'Профессиональная разработка Telegram ботов для автоматизации бизнеса',
                'description_en': 'Professional Telegram bot development for business automation',
                'description_de': 'Professionelle Telegram-Bot-Entwicklung für die Geschäftsautomatisierung',
                'description_ru': 'Профессиональная разработка Telegram ботов для автоматизации бизнеса',
                'is_active': True,
                'order': 1
            },
            {
                'name': 'Веб-сайти',
                'name_en': 'Websites',
                'name_de': 'Webseiten',
                'name_ru': 'Веб-сайты',
                'slug': 'websites',
                'description': 'Создание современных веб-сайтов и веб-приложений',
                'description_en': 'Creating modern websites and web applications',
                'description_de': 'Erstellung moderner Websites und Webanwendungen',
                'description_ru': 'Создание современных веб-сайтов и веб-приложений',
                'is_active': True,
                'order': 2
            },
            {
                'name': 'Мобільні додатки',
                'name_en': 'Mobile Apps',
                'name_de': 'Mobile Apps',
                'name_ru': 'Мобильные приложения',
                'slug': 'mobile-apps',
                'description': 'Разработка мобильных приложений для iOS и Android',
                'description_en': 'iOS and Android mobile app development',
                'description_de': 'iOS- und Android-App-Entwicklung',
                'description_ru': 'Разработка мобильных приложений для iOS и Android',
                'is_active': True,
                'order': 3
            }
        ]
        
        # Создаем категории
        categories = {}
        for cat_data in categories_data:
            category = Category.query.filter_by(slug=cat_data['slug']).first()
            if not category:
                category = Category(**cat_data)
                db.session.add(category)
                db.session.commit()
                print(f"Создана категория: {category.name}")
            categories[cat_data['slug']] = category
        
        # Создаем продукты
        products_data = [
            {
                'name': 'Базовий Telegram бот',
                'name_en': 'Basic Telegram Bot',
                'name_de': 'Basis Telegram Bot',
                'name_ru': 'Базовый Telegram бот',
                'slug': 'basic-telegram-bot',
                'description': 'Простой Telegram бот с основными функциями: приветствие, меню, FAQ, обратная связь',
                'description_en': 'Simple Telegram bot with basic features: greeting, menu, FAQ, feedback',
                'description_de': 'Einfacher Telegram-Bot mit Grundfunktionen: Begrüßung, Menü, FAQ, Feedback',
                'description_ru': 'Простой Telegram бот с основными функциями: приветствие, меню, FAQ, обратная связь',
                'category': categories['telegram-bots'],
                'price': 50.0,
                'token_price': 500.0,
                'delivery_time': '3-5 дней',
                'support_period': '1 месяц',
                'example_url': 'https://t.me/example_bot',
                'features': [
                    'Персонализированное приветствие',
                    'Интерактивное меню',
                    'База часто задаваемых вопросов',
                    'Форма обратной связи',
                    'Базовая аналитика'
                ],
                'is_digital': True,
                'is_active': True
            },
            {
                'name': 'Розширений Telegram бот',
                'name_en': 'Advanced Telegram Bot',
                'name_de': 'Erweiterte Telegram Bot',
                'name_ru': 'Расширенный Telegram бот',
                'slug': 'advanced-telegram-bot',
                'description': 'Профессиональный Telegram бот с интеграцией базы данных, платежами и админ-панелью',
                'description_en': 'Professional Telegram bot with database integration, payments, and admin panel',
                'description_de': 'Professioneller Telegram-Bot mit Datenbankintegration, Zahlungen und Admin-Panel',
                'description_ru': 'Профессиональный Telegram бот с интеграцией базы данных, платежами и админ-панелью',
                'category': categories['telegram-bots'],
                'price': 150.0,
                'token_price': 1500.0,
                'delivery_time': '7-10 дней',
                'support_period': '3 месяца',
                'example_url': 'https://t.me/advanced_example_bot',
                'features': [
                    'Интеграция с базой данных',
                    'Система платежей',
                    'Админ-панель',
                    'Многоязычность',
                    'Детальная аналитика',
                    'API интеграции',
                    'Уведомления'
                ],
                'is_digital': True,
                'is_active': True
            },
            {
                'name': 'Бізнес-сайт з CMS',
                'name_en': 'Business Website with CMS',
                'name_de': 'Business-Website mit CMS',
                'name_ru': 'Бизнес-сайт с CMS',
                'slug': 'business-website-cms',
                'description': 'Профессиональный бизнес-сайт с системой управления контентом и адаптивным дизайном',
                'description_en': 'Professional business website with content management system and responsive design',
                'description_de': 'Professionelle Business-Website mit Content-Management-System und responsivem Design',
                'description_ru': 'Профессиональный бизнес-сайт с системой управления контентом и адаптивным дизайном',
                'category': categories['websites'],
                'price': 300.0,
                'token_price': 3000.0,
                'delivery_time': '10-14 дней',
                'support_period': '6 месяцев',
                'example_url': 'https://example-business.com',
                'features': [
                    'Адаптивный дизайн',
                    'CMS для управления контентом',
                    'SEO оптимизация',
                    'Интеграция с соцсетями',
                    'Форма обратной связи',
                    'Google Analytics',
                    'SSL сертификат',
                    'Базовая SEO настройка'
                ],
                'is_digital': True,
                'is_active': True
            },
            {
                'name': 'Інтернет-магазин',
                'name_en': 'E-commerce Store',
                'name_de': 'E-Commerce-Shop',
                'name_ru': 'Интернет-магазин',
                'slug': 'ecommerce-store',
                'description': 'Полнофункциональный интернет-магазин с корзиной, платежами и админ-панелью',
                'description_en': 'Full-featured e-commerce store with cart, payments, and admin panel',
                'description_de': 'Voll ausgestatteter E-Commerce-Shop mit Warenkorb, Zahlungen und Admin-Panel',
                'description_ru': 'Полнофункциональный интернет-магазин с корзиной, платежами и админ-панелью',
                'category': categories['websites'],
                'price': 500.0,
                'token_price': 5000.0,
                'delivery_time': '14-21 день',
                'support_period': '12 месяцев',
                'example_url': 'https://example-shop.com',
                'features': [
                    'Каталог товаров',
                    'Корзина покупок',
                    'Интеграция платежей',
                    'Управление заказами',
                    'Личный кабинет',
                    'Система скидок',
                    'Многоязычность',
                    'Мобильная адаптация',
                    'SEO оптимизация'
                ],
                'is_digital': True,
                'is_active': True
            }
        ]
        
        # Создаем продукты
        for prod_data in products_data:
            product = Product.query.filter_by(slug=prod_data['slug']).first()
            if not product:
                category = prod_data.pop('category')
                product = Product(**prod_data)
                product.category_id = category.id
                db.session.add(product)
                db.session.commit()
                print(f"Создан продукт: {product.name}")
        
        print("Демонстрационные данные созданы успешно!")

if __name__ == "__main__":
    create_demo_products()
