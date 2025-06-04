#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Создание демо-данных для аирдропа, DAO и токенсейла
"""

from app import create_app, db
from app.models import Airdrop, TokenSale, DaoProposal, Token
from datetime import datetime, timedelta
import pytz

app = create_app()

def create_blockchain_demo_data():
    """Создает демо-данные для аирдропа, DAO и токенсейла"""
    print("=" * 60)
    print("СОЗДАНИЕ ДЕМО-ДАННЫХ ДЛЯ БЛОКЧЕЙН ФУНКЦИОНАЛА")
    print("=" * 60)
    
    with app.app_context():
        # Текущая дата и будущие даты для мероприятий
        now = datetime.now(pytz.UTC)
        one_week_later = now + timedelta(days=7)
        two_weeks_later = now + timedelta(days=14)
        month_later = now + timedelta(days=30)
        
        # 1. Создание аирдропов
        print("\n1. Создание демо-аирдропов...")
        
        # Проверяем существующие аирдропы
        existing_airdrops = Airdrop.query.all()
        if existing_airdrops:
            print(f"Найдено {len(existing_airdrops)} существующих аирдропов")
        else:
            print("Аирдропов не найдено, создаем демо-аирдропы")
            
            # Аирдроп 1: Активный
            airdrop1 = Airdrop(
                title="Аирдроп для ранних участников",
                title_ua="Аирдроп для ранніх учасників",
                title_en="Early Adopters Airdrop",
                title_de="Airdrop für frühe Teilnehmer",
                title_ru="Аирдроп для ранних участников",
                description="Получите 100 IT TOKEN бесплатно за регистрацию на нашей платформе и подключение кошелька.",
                description_ua="Отримайте 100 IT TOKEN безкоштовно за реєстрацію на нашій платформі та підключення гаманця.",
                description_en="Get 100 IT TOKEN free for registering on our platform and connecting your wallet.",
                description_de="Erhalten Sie 100 IT TOKEN kostenlos für die Registrierung auf unserer Plattform und die Verbindung Ihrer Wallet.",
                description_ru="Получите 100 IT TOKEN бесплатно за регистрацию на нашей платформе и подключение кошелька.",
                total_amount=10000.0,
                amount_per_user=100.0,
                start_date=now - timedelta(days=7),
                end_date=one_week_later,
                is_active=True
            )
            db.session.add(airdrop1)
            
            # Аирдроп 2: Будущий
            airdrop2 = Airdrop(
                title="Аирдроп для держателей токенов",
                title_ua="Аирдроп для власників токенів",
                title_en="Token Holders Airdrop",
                title_de="Airdrop für Token-Inhaber",
                title_ru="Аирдроп для держателей токенов",
                description="Держатели токенов IT TOKEN получат дополнительные токены в зависимости от количества токенов на балансе.",
                description_ua="Власники токенів IT TOKEN отримають додаткові токени в залежності від кількості токенів на балансі.",
                description_en="IT TOKEN holders will receive additional tokens based on the number of tokens in their balance.",
                description_de="IT TOKEN-Inhaber erhalten zusätzliche Token basierend auf der Anzahl der Token in ihrem Guthaben.",
                description_ru="Держатели токенов IT TOKEN получат дополнительные токены в зависимости от количества токенов на балансе.",
                total_amount=50000.0,
                amount_per_user=200.0,
                start_date=one_week_later,
                end_date=month_later,
                is_active=True
            )
            db.session.add(airdrop2)
            db.session.commit()
            print("✅ Созданы 2 демо-аирдропа")
        
        # 2. Создание токенсейлов
        print("\n2. Создание демо-токенсейлов...")
        
        # Проверяем существующие токенсейлы
        existing_tokensales = TokenSale.query.all()
        if existing_tokensales:
            print(f"Найдено {len(existing_tokensales)} существующих токенсейлов")
        else:
            print("Токенсейлов не найдено, создаем демо-токенсейлы")
            
            # Токенсейл 1: Активный
            tokensale1 = TokenSale(
                title="Предварительная продажа IT TOKEN",
                title_ua="Попередній продаж IT TOKEN",
                title_en="IT TOKEN Presale",
                title_de="IT TOKEN Vorverkauf",
                title_ru="Предварительная продажа IT TOKEN",
                description="Участвуйте в предварительной продаже токенов IT TOKEN по специальной цене 0.08 USD за токен.",
                description_ua="Беріть участь у попередньому продажу токенів IT TOKEN за спеціальною ціною 0.08 USD за токен.",
                description_en="Participate in the IT TOKEN presale at a special price of $0.08 per token.",
                description_de="Nehmen Sie am IT TOKEN-Vorverkauf zum Sonderpreis von 0,08 USD pro Token teil.",
                description_ru="Участвуйте в предварительной продаже токенов IT TOKEN по специальной цене 0.08 USD за токен.",
                total_amount=200000.0,
                price=0.08,
                min_purchase=100.0,
                max_purchase=10000.0,
                start_date=now - timedelta(days=3),
                end_date=two_weeks_later,
                is_active=True
            )
            db.session.add(tokensale1)
            
            # Токенсейл 2: Будущий
            tokensale2 = TokenSale(
                title="Публичная продажа IT TOKEN",
                title_ua="Публічний продаж IT TOKEN",
                title_en="IT TOKEN Public Sale",
                title_de="IT TOKEN Öffentlicher Verkauf",
                title_ru="Публичная продажа IT TOKEN",
                description="Публичная продажа токенов IT TOKEN по цене 0.1 USD за токен. Количество токенов ограничено.",
                description_ua="Публічний продаж токенів IT TOKEN за ціною 0.1 USD за токен. Кількість токенів обмежена.",
                description_en="Public sale of IT TOKEN at a price of $0.1 per token. The number of tokens is limited.",
                description_de="Öffentlicher Verkauf von IT TOKEN zum Preis von 0,1 USD pro Token. Die Anzahl der Token ist begrenzt.",
                description_ru="Публичная продажа токенов IT TOKEN по цене 0.1 USD за токен. Количество токенов ограничено.",
                total_amount=500000.0,
                price=0.1,
                min_purchase=50.0,
                max_purchase=50000.0,
                start_date=two_weeks_later,
                end_date=month_later,
                is_active=True
            )
            db.session.add(tokensale2)
            db.session.commit()
            print("✅ Созданы 2 демо-токенсейла")
        
        # 3. Создание DAO-предложений
        print("\n3. Создание DAO-предложений...")
        
        # Проверяем существующие DAO-предложения
        existing_proposals = DaoProposal.query.all()
        if existing_proposals:
            print(f"Найдено {len(existing_proposals)} существующих DAO-предложений")
        else:
            print("DAO-предложений не найдено, создаем демо-предложения")
            
            # DAO-предложение 1: Активное
            proposal1 = DaoProposal(
                title="Листинг токена IT TOKEN на биржах",
                title_ua="Лістинг токена IT TOKEN на біржах",
                title_en="Listing IT TOKEN on exchanges",
                title_de="Notierung von IT TOKEN an Börsen",
                title_ru="Листинг токена IT TOKEN на биржах",
                description="Предложение об использовании средств из казны проекта для листинга токена IT TOKEN на централизованных биржах.",
                description_ua="Пропозиція щодо використання коштів з казни проекту для лістингу токена IT TOKEN на централізованих біржах.",
                description_en="A proposal to use funds from the project treasury to list IT TOKEN on centralized exchanges.",
                description_de="Ein Vorschlag zur Verwendung von Mitteln aus dem Projektbudget für die Notierung von IT TOKEN an zentralisierten Börsen.",
                description_ru="Предложение об использовании средств из казны проекта для листинга токена IT TOKEN на централизованных биржах.",
                start_date=now - timedelta(days=5),
                end_date=one_week_later,
                min_tokens_to_vote=10.0,
                status='active',
                votes_for=120,
                votes_against=30,
                author_id=None  # Будет назначен позже, после создания пользователей
            )
            db.session.add(proposal1)
            
            # DAO-предложение 2: Планируемое
            proposal2 = DaoProposal(
                title="Обновление смарт-контракта токена",
                title_ua="Оновлення смарт-контракту токена",
                title_en="Token smart contract upgrade",
                title_de="Upgrade des Token-Smart-Contracts",
                title_ru="Обновление смарт-контракта токена",
                description="Предложение об обновлении смарт-контракта токена для добавления новых функций и улучшения безопасности.",
                description_ua="Пропозиція щодо оновлення смарт-контракту токена для додавання нових функцій та покращення безпеки.",
                description_en="A proposal to upgrade the token smart contract to add new features and improve security.",
                description_de="Ein Vorschlag zur Aktualisierung des Token-Smart-Contracts, um neue Funktionen hinzuzufügen und die Sicherheit zu verbessern.",
                description_ru="Предложение об обновлении смарт-контракта токена для добавления новых функций и улучшения безопасности.",
                start_date=one_week_later,
                end_date=two_weeks_later,
                min_tokens_to_vote=5.0,
                status='pending',
                votes_for=0,
                votes_against=0,
                author_id=None  # Будет назначен позже, после создания пользователей
            )
            db.session.add(proposal2)
            db.session.commit()
            print("✅ Созданы 2 демо-DAO-предложения")
        
        # 4. Обновление данных токена, если нужно
        token = Token.query.first()
        if token:
            print("\n4. Обновление данных токена...")
            token.total_supply = 1000000.0
            token.circulating_supply = 250000.0
            token.token_price_usd = 0.1
            db.session.commit()
            print("✅ Данные токена обновлены")
        
        print("\n" + "=" * 60)
        print("✅ СОЗДАНИЕ ДЕМО-ДАННЫХ ЗАВЕРШЕНО")
        print("=" * 60)
        
        # Выводим сводку созданных объектов
        print("\nДемо-данные в базе данных:")
        print(f"- Аирдропы: {Airdrop.query.count()}")
        print(f"- Токенсейлы: {TokenSale.query.count()}")
        print(f"- DAO-предложения: {DaoProposal.query.count()}")

if __name__ == "__main__":
    create_blockchain_demo_data()
