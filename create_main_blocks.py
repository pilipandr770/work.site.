#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создание основных блоков сайта:
1. Главный блок (Баннер)
2. Аирдроп
3. Токенсейл
4. DAO (Управление)
5. Магазин
6. Платежи
"""

from app import create_app, db
from app.models import Block, Settings, Token
from datetime import datetime
import uuid

app = create_app()

def create_main_blocks():
    """Создает основные блоки сайта, если они не существуют"""
    print("Создаем основные блоки сайта...")
    
    with app.app_context():
        # Проверяем настройки сайта
        settings = Settings.query.first()
        if not settings:
            print("Создаем основные настройки сайта...")
            settings = Settings(
                facebook="https://facebook.com/yourproject",
                instagram="https://instagram.com/yourproject",
                telegram="https://t.me/yourproject",
                email="info@yourproject.com",
                contract_address="0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d",
                token_name="IT TOKEN",
                token_symbol="ITT",
                network_rpc="https://polygon-mumbai.infura.io/v3/YOUR_API_KEY",
                network_chain_id=80001
            )
            db.session.add(settings)
            db.session.commit()
            print("✅ Настройки сайта созданы")
            
        # Проверяем информацию о токене
        token = Token.query.first()
        if not token:
            print("Создаем информацию о токене...")
            token = Token(
                name="IT TOKEN",
                symbol="ITT",
                contract_address="0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d",
                decimals=18,
                total_supply=1000000.0,
                circulating_supply=500000.0,
                token_price_usd=0.1,
                description="IT TOKEN - это токен проекта, который используется для различных операций на платформе.",
                description_ua="IT TOKEN - це токен проекту, який використовується для різноманітних операцій на платформі.",
                description_en="IT TOKEN is the project's token used for various operations on the platform.",
                description_de="IT TOKEN ist der Token des Projekts, der für verschiedene Operationen auf der Plattform verwendet wird.",
                description_ru="IT TOKEN - это токен проекта, который используется для различных операций на платформе."
            )
            db.session.add(token)
            db.session.commit()
            print("✅ Информация о токене создана")
        
        # Создаем блоки если они не существуют
        blocks_to_create = [
            # 1. Главный блок
            {
                "title": "Блокчейн решения для вашего бизнеса",
                "title_en": "Blockchain solutions for your business",
                "title_de": "Blockchain-Lösungen für Ihr Unternehmen",
                "title_ru": "Блокчейн решения для вашего бизнеса",
                "content": "IT TOKEN предоставляет современные блокчейн решения для вашего бизнеса. Мы помогаем внедрить токенизацию, создать DAO и запустить децентрализованные приложения.",
                "content_en": "IT TOKEN provides modern blockchain solutions for your business. We help implement tokenization, create a DAO, and launch decentralized applications.",
                "content_de": "IT TOKEN bietet moderne Blockchain-Lösungen für Ihr Unternehmen. Wir helfen bei der Implementierung von Tokenisierung, der Erstellung einer DAO und dem Start von dezentralen Anwendungen.",
                "content_ru": "IT TOKEN предоставляет современные блокчейн решения для вашего бизнеса. Мы помогаем внедрить токенизацию, создать DAO и запустить децентрализованные приложения.",
                "slug": "main-banner",
                "order": 1,
                "is_top": True
            },
            # 2. Блок Аирдроп
            {
                "title": "Аирдроп IT TOKEN",
                "title_en": "IT TOKEN Airdrop",
                "title_de": "IT TOKEN Airdrop",
                "title_ru": "Аирдроп IT TOKEN",
                "content": "Участвуйте в аирдропе токенов IT TOKEN. Получите бесплатные токены для использования на нашей платформе.",
                "content_en": "Participate in the IT TOKEN airdrop. Get free tokens to use on our platform.",
                "content_de": "Nehmen Sie am IT TOKEN Airdrop teil. Erhalten Sie kostenlose Tokens für die Nutzung auf unserer Plattform.",
                "content_ru": "Участвуйте в аирдропе токенов IT TOKEN. Получите бесплатные токены для использования на нашей платформе.",
                "slug": "airdrop",
                "order": 2
            },
            # 3. Блок Токенсейл
            {
                "title": "Продажа токенов IT TOKEN",
                "title_en": "IT TOKEN Sale",
                "title_de": "IT TOKEN Verkauf",
                "title_ru": "Продажа токенов IT TOKEN",
                "content": "Приобретайте токены IT TOKEN на ранней стадии проекта по выгодной цене. Инвестируйте в будущее технологий.",
                "content_en": "Buy IT TOKEN tokens at an early stage of the project at a favorable price. Invest in the future of technology.",
                "content_de": "Kaufen Sie IT TOKEN in einer frühen Phase des Projekts zu einem günstigen Preis. Investieren Sie in die Zukunft der Technologie.",
                "content_ru": "Приобретайте токены IT TOKEN на ранней стадии проекта по выгодной цене. Инвестируйте в будущее технологий.",
                "slug": "token-sale",
                "order": 3
            },
            # 4. Блок DAO
            {
                "title": "Управление проектом (DAO)",
                "title_en": "Project Governance (DAO)",
                "title_de": "Projektverwaltung (DAO)",
                "title_ru": "Управление проектом (DAO)",
                "content": "Участвуйте в управлении проектом через нашу децентрализованную автономную организацию (DAO). Ваши токены - ваш голос в принятии важных решений.",
                "content_en": "Participate in project governance through our decentralized autonomous organization (DAO). Your tokens are your voice in making important decisions.",
                "content_de": "Beteiligen Sie sich an der Projektverwaltung durch unsere dezentralisierte autonome Organisation (DAO). Ihre Tokens sind Ihre Stimme bei wichtigen Entscheidungen.",
                "content_ru": "Участвуйте в управлении проектом через нашу децентрализованную автономную организацию (DAO). Ваши токены - ваш голос в принятии важных решений.",
                "slug": "dao",
                "order": 4
            },
            # 5. Блок Магазин
            {
                "title": "Магазин цифровых товаров",
                "title_en": "Digital Goods Store",
                "title_de": "Digitaler Warengeschäft",
                "title_ru": "Магазин цифровых товаров",
                "content": "Приобретайте наши цифровые товары и услуги за фиатные деньги или токены IT TOKEN. У нас представлены веб-сайты, боты, интеграции и консультации.",
                "content_en": "Purchase our digital goods and services for fiat money or IT TOKEN tokens. We offer websites, bots, integrations, and consultations.",
                "content_de": "Kaufen Sie unsere digitalen Waren und Dienstleistungen für Fiat-Geld oder IT TOKEN. Wir bieten Websites, Bots, Integrationen und Beratungen an.",
                "content_ru": "Приобретайте наши цифровые товары и услуги за фиатные деньги или токены IT TOKEN. У нас представлены веб-сайты, боты, интеграции и консультации.",
                "slug": "shop",
                "order": 5
            },
            # 6. Блок Платежи
            {
                "title": "Платежные решения",
                "title_en": "Payment Solutions",
                "title_de": "Zahlungslösungen",
                "title_ru": "Платежные решения",
                "content": "Удобные способы оплаты для наших клиентов. Принимаем криптовалюты, банковские переводы и платежи картами.",
                "content_en": "Convenient payment methods for our clients. We accept cryptocurrencies, bank transfers, and card payments.",
                "content_de": "Bequeme Zahlungsmethoden für unsere Kunden. Wir akzeptieren Kryptowährungen, Banküberweisungen und Kartenzahlungen.",
                "content_ru": "Удобные способы оплаты для наших клиентов. Принимаем криптовалюты, банковские переводы и платежи картами.",
                "slug": "payment",
                "order": 6
            }
        ]
        
        created_count = 0
        for block_data in blocks_to_create:
            # Проверяем наличие блока по slug
            existing_block = Block.query.filter_by(slug=block_data["slug"]).first()
            if not existing_block:
                # Создаем новый блок
                new_block = Block(
                    title=block_data["title"],
                    title_ua=block_data["title"],
                    title_en=block_data["title_en"],
                    title_de=block_data["title_de"],
                    title_ru=block_data["title_ru"],
                    content=block_data["content"],
                    content_ua=block_data["content"],
                    content_en=block_data["content_en"],
                    content_de=block_data["content_de"],
                    content_ru=block_data["content_ru"],
                    slug=block_data["slug"],
                    order=block_data["order"],
                    is_active=True,
                    is_top=block_data.get("is_top", False)
                )
                db.session.add(new_block)
                created_count += 1
                print(f"✅ Создан блок: {block_data['title']}")
        
        if created_count > 0:
            db.session.commit()
            print(f"✅ Всего создано блоков: {created_count}")
        else:
            print("ℹ️ Все блоки уже существуют, новые блоки не создавались.")
        
        # Выводим список всех блоков
        all_blocks = Block.query.order_by(Block.order).all()
        print("\nВсе блоки сайта:")
        for block in all_blocks:
            print(f"ID: {block.id}, Заголовок: {block.title}, Slug: {block.slug}, Активен: {block.is_active}, Главный: {block.is_top}")

if __name__ == "__main__":
    create_main_blocks()
