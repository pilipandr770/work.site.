#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для инициализации данных на Render.com
Создает основные блоки, настройки и токены, если они не существуют
"""

from app import create_app, db
from app.models import Block, Settings, Token
import os
import sys
from datetime import datetime

app = create_app()

def initialize_data():
    """Инициализирует основные данные для работы сайта"""
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ ДАННЫХ ДЛЯ RENDER.COM")
    print("=" * 60)
    
    with app.app_context():
        # Получаем настройки контракта из переменных окружения
        contract_address = os.environ.get("TOKEN_CONTRACT_ADDRESS", "0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d")
        receiver_address = os.environ.get("TOKEN_RECEIVER_ADDRESS", "0x917544120060Feb4571CdB14dBCC1e4d8005c218")
        
        # 1. Обновляем настройки сайта
        print("\n1. Обновление настроек сайта...")
        settings = Settings.query.first()
        if not settings:
            settings = Settings()
        
        settings.facebook = "https://facebook.com/ittoken"
        settings.instagram = "https://instagram.com/ittoken"
        settings.telegram = "https://t.me/ittoken"
        settings.email = "info@ittoken.com"
        settings.contract_address = contract_address
        settings.token_name = "IT TOKEN"
        settings.token_symbol = "ITT"
        settings.network_rpc = "https://polygon-mumbai.g.alchemy.com/v2/YOUR-API-KEY"
        settings.network_chain_id = 80001
        
        db.session.add(settings)
        db.session.commit()
        print("✅ Настройки сайта обновлены")
        
        # 2. Обновляем информацию о токене
        print("\n2. Обновление информации о токене...")
        token = Token.query.first()
        if not token:
            token = Token(
                name="IT TOKEN",
                symbol="ITT",
                contract_address=contract_address,
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
        else:
            token.contract_address = contract_address
            db.session.commit()
            print("✅ Информация о токене обновлена")
        
        # 3. Создаем основные блоки
        print("\n3. Создание основных блоков...")
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
        updated_count = 0
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
            else:
                # Обновляем существующий блок, но только если он не был модифицирован вручную
                # (проверка на измененное содержание)
                if existing_block.title == existing_block.title_ua:  # Если заголовок не был изменен вручную
                    existing_block.title = block_data["title"]
                    existing_block.title_ua = block_data["title"]
                    existing_block.title_en = block_data["title_en"]
                    existing_block.title_de = block_data["title_de"]
                    existing_block.title_ru = block_data["title_ru"]
                    
                    if existing_block.content == existing_block.content_ua:  # Если содержимое не было изменено вручную
                        existing_block.content = block_data["content"]
                        existing_block.content_ua = block_data["content"]
                        existing_block.content_en = block_data["content_en"]
                        existing_block.content_de = block_data["content_de"]
                        existing_block.content_ru = block_data["content_ru"]
                    
                    existing_block.order = block_data["order"]
                    if "is_top" in block_data:
                        existing_block.is_top = block_data["is_top"]
                    
                    updated_count += 1
                    print(f"✅ Обновлен блок: {block_data['title']}")
        
        if created_count > 0 or updated_count > 0:
            db.session.commit()
            print(f"\n✅ Всего создано блоков: {created_count}")
            print(f"✅ Всего обновлено блоков: {updated_count}")
        else:
            print("\nℹ️ Все блоки актуальны, изменения не требуются.")
        
        # Выводим список всех блоков
        all_blocks = Block.query.order_by(Block.order).all()
        print("\nТекущие блоки сайта:")
        for block in all_blocks:
            status = "✅" if block.is_active else "❌"
            top_status = "⭐" if block.is_top else " "
            print(f"{status} {top_status} ID: {block.id}, Заголовок: {block.title}, Slug: {block.slug}")
    
    print("\n" + "=" * 60)
    print("✅ ИНИЦИАЛИЗАЦИЯ ДАННЫХ ЗАВЕРШЕНА")
    print("=" * 60)

if __name__ == "__main__":
    initialize_data()
