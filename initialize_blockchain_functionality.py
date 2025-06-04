from app import create_app, db
from app.models import Token, Airdrop, TokenSale, DaoProposal
from datetime import datetime, timedelta
import os
import pytz

app = create_app()

def initialize_blockchain_functionality():
    """Инициализирует минимально необходимые данные для работы блокчейн-функционала"""
    print("=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ БЛОКЧЕЙН-ФУНКЦИОНАЛА")
    print("=" * 60)
    
    with app.app_context():
        # Получаем реальный адрес токена из переменной окружения
        token_address = os.environ.get('TOKEN_CONTRACT_ADDRESS', '0xAf6087a1A730DAb2CA8d42dca7893c22fDBA683d')
        print(f"Используем адрес контракта токена: {token_address}")
        
        # Обновляем или создаем запись токена с правильным адресом контракта
        token = Token.query.first()
        if token:
            if token.contract_address != token_address:
                token.contract_address = token_address
                db.session.commit()
                print(f"✅ Обновлен адрес токен-контракта: {token_address}")
        else:
            # Создаем токен, если его еще нет
            token = Token(
                name="IT TOKEN",
                symbol="ITT",
                contract_address=token_address,
                decimals=18,
                total_supply=1000000,
                circulating_supply=700000,
                token_price_usd=0.1,
                description="Токен экосистемы IT Shop для оплаты товаров, участия в DAO и получения вознаграждений.",
                description_ua="Токен екосистеми IT Shop для оплати товарів, участі в DAO та отримання винагород.",
                description_en="IT Shop ecosystem token for paying goods, participating in DAO and earning rewards.",
                description_de="IT Shop Ökosystem-Token für die Bezahlung von Waren, die Teilnahme an DAO und das Verdienen von Belohnungen.",
                description_ru="Токен экосистемы IT Shop для оплаты товаров, участия в DAO и получения вознаграждений."
            )
            db.session.add(token)
            db.session.commit()
            print(f"✅ Создан новый токен: {token.name} ({token.symbol}) с адресом контракта: {token_address}")
        
        # Текущая дата и будущие даты для мероприятий
        now = datetime.now(pytz.UTC)
        one_week_later = now + timedelta(days=7)
        two_weeks_later = now + timedelta(days=14)
        
        # 1. Создание аирдропа, если его нет
        if Airdrop.query.count() == 0:
            print("\n1. Создание аирдропа...")
            airdrop = Airdrop(
                title="IT TOKEN Airdrop",
                title_ua="IT TOKEN Аирдроп",
                title_en="IT TOKEN Airdrop",
                title_de="IT TOKEN Airdrop",
                title_ru="IT TOKEN Аирдроп",
                description="Получите токены IT TOKEN за участие в проекте",
                description_ua="Отримайте токени IT TOKEN за участь у проекті",
                description_en="Get IT TOKEN tokens for participating in the project",
                description_de="Erhalten Sie IT TOKEN für die Teilnahme am Projekt",
                description_ru="Получите токены IT TOKEN за участие в проекте",
                total_amount=10000.0,
                amount_per_user=100.0,
                start_date=now,
                end_date=one_week_later,
                is_active=True
            )
            db.session.add(airdrop)
            db.session.commit()
            print(f"✅ Создан аирдроп: {airdrop.title}")
        else:
            print("Аирдроп уже существует")
        
        # 2. Создание токенсейла, если его нет
        if TokenSale.query.count() == 0:
            print("\n2. Создание токенсейла...")
            tokensale = TokenSale(
                title="IT TOKEN Sale",
                title_ua="Продаж IT TOKEN",
                title_en="IT TOKEN Sale",
                title_de="IT TOKEN Verkauf",
                title_ru="Продажа IT TOKEN",
                description="Приобретайте токены IT TOKEN",
                description_ua="Придбайте токени IT TOKEN",
                description_en="Purchase IT TOKEN tokens",
                description_de="Kaufen Sie IT TOKEN",
                description_ru="Приобретайте токены IT TOKEN",
                total_amount=100000.0,
                price=0.1,
                min_purchase=10.0,
                max_purchase=1000.0,
                start_date=now,
                end_date=one_week_later,
                is_active=True
            )
            db.session.add(tokensale)
            db.session.commit()
            print(f"✅ Создан токенсейл: {tokensale.title}")
        else:
            print("Токенсейл уже существует")
        
        # 3. Создание DAO-предложения, если его нет
        if DaoProposal.query.count() == 0:
            print("\n3. Создание DAO-предложения...")
            proposal = DaoProposal(
                title="Развитие проекта IT TOKEN",
                title_ua="Розвиток проекту IT TOKEN",
                title_en="IT TOKEN Project Development",
                title_de="IT TOKEN Projektentwicklung",
                title_ru="Развитие проекта IT TOKEN",
                description="Предложение по развитию проекта IT TOKEN",
                description_ua="Пропозиція щодо розвитку проекту IT TOKEN",
                description_en="Proposal for IT TOKEN project development",
                description_de="Vorschlag zur Entwicklung des IT TOKEN-Projekts",
                description_ru="Предложение по развитию проекта IT TOKEN",
                start_date=now,
                end_date=two_weeks_later,
                min_tokens_to_vote=1.0,
                status='active',
                votes_for=10,
                votes_against=2
            )
            db.session.add(proposal)
            db.session.commit()
            print(f"✅ Создано DAO-предложение: {proposal.title}")
        else:
            print("DAO-предложение уже существует")
        
        print("\n" + "=" * 60)
        print("✅ ИНИЦИАЛИЗАЦИЯ БЛОКЧЕЙН-ФУНКЦИОНАЛА ЗАВЕРШЕНА")
        print("=" * 60)
        
        # Выводим сводку созданных объектов
        airdrops = Airdrop.query.all()
        print(f"\nАирдропы: {len(airdrops)}")
        for a in airdrops:
            print(f"  - {a.title} (ID: {a.id}, Активен: {a.is_active})")
            
        tokensales = TokenSale.query.all()
        print(f"\nТокенсейлы: {len(tokensales)}")
        for t in tokensales:
            print(f"  - {t.title} (ID: {t.id}, Активен: {t.is_active})")
            
        proposals = DaoProposal.query.all()
        print(f"\nDAO-предложения: {len(proposals)}")
        for p in proposals:
            print(f"  - {p.title} (ID: {p.id}, Статус: {p.status})")

if __name__ == "__main__":
    initialize_blockchain_functionality()
