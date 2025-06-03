from app.models import User, Block, Settings, Token, Airdrop, TokenSale, DaoProposal
from app.models import Category, Product
from app import db
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Создает демоданные для проекта"""
    print("Создание демоданных для проекта...")    # Очистка связанных таблиц (сначала дочерние, потом родительские)
    db.session.query(Product).delete()
    db.session.query(Category).delete()
    db.session.query(DaoProposal).delete()
    db.session.query(TokenSale).delete()
    db.session.query(Airdrop).delete()
    db.session.query(Token).delete()
    db.session.query(Block).delete()
    db.session.commit()
    
    # Создаем токен
    token = Token(
        name="IT Shop Token",
        symbol="ITST",
        contract_address="0x1234567890123456789012345678901234567890",
        decimals=18,
        total_supply=1000000,
        circulating_supply=300000,
        token_price_usd=0.10,
        description="""IT Shop Token (ITST) - это утилити-токен нашей экосистемы IT-услуг и товаров.
            Токен позволяет получать скидки на все товары и услуги, участвовать в управлении 
            проектом через DAO, а также получать вознаграждение за участие в развитии экосистемы.""",
        description_ua="""IT Shop Token (ITST) - це утіліті-токен нашої екосистеми ІТ-послуг та товарів.
            Токен дозволяє отримувати знижки на всі товари та послуги, брати участь в управлінні 
            проектом через DAO, а також отримувати винагороду за участь у розвитку екосистеми.""",
        description_en="""IT Shop Token (ITST) is the utility token for our ecosystem of IT services and products.
            The token allows you to get discounts on all products and services, participate in project management 
            through DAO, and receive rewards for participating in the development of the ecosystem.""",
        description_de="""IT Shop Token (ITST) ist der Utility-Token für unser Ökosystem von IT-Dienstleistungen und -Produkten.
            Der Token ermöglicht es Ihnen, Rabatte auf alle Produkte und Dienstleistungen zu erhalten, an der Projektverwaltung 
            über DAO teilzunehmen und Belohnungen für die Teilnahme an der Entwicklung des Ökosystems zu erhalten.""",
        description_ru="""IT Shop Token (ITST) - это утилитарный токен нашей экосистемы IT-услуг и товаров.
            Токен позволяет получать скидки на все товары и услуги, участвовать в управлении 
            проектом через DAO, а также получать вознаграждение за участие в развитии экосистемы."""
    )
    db.session.add(token)
    
    # Создаем аирдроп
    airdrop = Airdrop(
        title="First Community Airdrop",
        description="""Примите участие в нашем первом аирдропе и получите 100 ITST токенов!
            Для участия просто подключите ваш кошелек и зарегистрируйтесь.""",
        total_amount=50000,
        amount_per_user=100,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=30),
        is_active=True,
        title_ua="Перший Аірдроп для Спільноти",
        title_en="First Community Airdrop",
        title_de="Erster Community Airdrop", 
        title_ru="Первый Аирдроп для Сообщества",
        description_ua="""Візьміть участь у нашому першому аірдропі та отримайте 100 ITST токенів!
            Для участі просто підключіть ваш гаманець та зареєструйтесь.""",
        description_en="""Take part in our first airdrop and get 100 ITST tokens!
            To participate, simply connect your wallet and register.""",
        description_de="""Nehmen Sie an unserem ersten Airdrop teil und erhalten Sie 100 ITST-Token!
            Um teilzunehmen, verbinden Sie einfach Ihre Wallet und registrieren Sie sich.""",
        description_ru="""Примите участие в нашем первом аирдропе и получите 100 ITST токенов!
            Для участия просто подключите ваш кошелек и зарегистрируйтесь."""
    )
    db.session.add(airdrop)
    
    # Создаем токенсейл
    token_sale = TokenSale(
        title="Public Token Sale",
        description="""Участвуйте в публичной продаже токенов ITST! Эта распродажа предлагает токены 
            по наиболее выгодной цене. Минимальная покупка - 100 токенов, максимальная - 10000 токенов.""",
        total_amount=200000,
        price=0.05,
        min_purchase=100,
        max_purchase=10000,
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=60),
        is_active=True,
        title_ua="Публічний Продаж Токенів",
        title_en="Public Token Sale",
        title_de="Öffentlicher Token-Verkauf",
        title_ru="Публичная Продажа Токенов",
        description_ua="""Беріть участь у публічному продажу токенів ITST! Цей розпродаж пропонує токени 
            за найбільш вигідною ціною. Мінімальна покупка - 100 токенів, максимальна - 10000 токенів.""",
        description_en="""Participate in the public sale of ITST tokens! This sale offers tokens 
            at the most favorable price. Minimum purchase is 100 tokens, maximum is 10000 tokens.""",
        description_de="""Nehmen Sie am öffentlichen Verkauf von ITST-Token teil! Dieser Verkauf bietet Token 
            zum günstigsten Preis. Mindestabnahme sind 100 Token, maximal 10000 Token.""",
        description_ru="""Участвуйте в публичной продаже токенов ITST! Эта распродажа предлагает токены 
            по наиболее выгодной цене. Минимальная покупка - 100 токенов, максимальная - 10000 токенов."""
    )
    db.session.add(token_sale)
    
    # Создаем DAO предложение
    proposal = DaoProposal(
        title="Listing on a Top 10 Exchange",
        description="""This proposal suggests allocating $50,000 from the treasury to cover the listing fee 
            for our token on one of the Top 10 cryptocurrency exchanges. This will increase liquidity and 
            visibility of our token.""",
        author_id=1,  # Предполагаем, что админ с ID=1 уже существует
        start_date=datetime.now(),
        end_date=datetime.now() + timedelta(days=14),
        min_tokens_to_vote=100,
        status="active",
        votes_for=1200,
        votes_against=300,
        title_ua="Лістинг на Топ-10 Біржі",
        title_en="Listing on a Top 10 Exchange",
        title_de="Börsennotierung an einer Top-10-Börse",
        title_ru="Листинг на Топ-10 Бирже",
        description_ua="""Ця пропозиція пропонує виділити 50 000 доларів з скарбниці для покриття комісії 
            за лістинг нашого токена на одній з Топ-10 криптовалютних бірж. Це збільшить ліквідність та 
            видимість нашого токена.""",
        description_en="""This proposal suggests allocating $50,000 from the treasury to cover the listing fee 
            for our token on one of the Top 10 cryptocurrency exchanges. This will increase liquidity and 
            visibility of our token.""",
        description_de="""Dieser Vorschlag schlägt vor, 50.000 $ aus der Schatzkammer zuzuweisen, um die Notierungsgebühr 
            für unser Token an einer der Top 10 Kryptowährungsbörsen zu decken. Dies wird die Liquidität und 
            Sichtbarkeit unseres Tokens erhöhen.""",
        description_ru="""Это предложение предлагает выделить $50,000 из казначейства для покрытия комиссии 
            за листинг нашего токена на одной из Топ-10 криптовалютных бирж. Это увеличит ликвидность и 
            видимость нашего токена."""
    )
    db.session.add(proposal)
    
    # Создаем категории продуктов
    categories = [
        Category(
            name="Боты",
            slug="bots",
            description="Telegram боты, Discord боты и другие автоматизированные решения",
            is_active=True,
            order=1,
            name_ua="Боти",
            name_en="Bots",
            name_de="Bots", 
            name_ru="Боты",
            description_ua="Telegram боти, Discord боти та інші автоматизовані рішення",
            description_en="Telegram bots, Discord bots and other automated solutions",
            description_de="Telegram-Bots, Discord-Bots und andere automatisierte Lösungen",
            description_ru="Telegram боты, Discord боты и другие автоматизированные решения"
        ),
        Category(
            name="Сайты",
            slug="websites",
            description="Создание современных веб-сайтов любой сложности",
            is_active=True,
            order=2,
            name_ua="Сайти",
            name_en="Websites",
            name_de="Webseiten",
            name_ru="Сайты",
            description_ua="Створення сучасних веб-сайтів будь-якої складності",
            description_en="Creation of modern websites of any complexity",
            description_de="Erstellung moderner Websites jeder Комлексität",
            description_ru="Создание современных веб-сайтов любой сложности"
        ),
        Category(
            name="Приложения",
            slug="apps",
            description="Мобильные приложения для iOS и Android",
            is_active=True,
            order=3,
            name_ua="Додатки",
            name_en="Apps",
            name_de="Apps",
            name_ru="Приложения",
            description_ua="Мобільні додатки для iOS та Android",
            description_en="Mobile applications for iOS and Android",
            description_de="Mobile Anwendungen für iOS und Android",
            description_ru="Мобильные приложения для iOS и Android"
        )
    ]
    for category in categories:
        db.session.add(category)
    
    db.session.commit()  # Сохраняем категории, чтобы получить их ID
    
    # Получаем ID категорий
    bots_category = Category.query.filter_by(slug="bots").first()
    websites_category = Category.query.filter_by(slug="websites").first()
    apps_category = Category.query.filter_by(slug="apps").first()
    
    # Создаем продукты
    products = [
        Product(
            name="Telegram бот для бизнеса",
            slug="telegram-bot-business",
            description="""Полнофункциональный Telegram бот для вашего бизнеса с возможностями 
                приема заказов, обработки платежей и интеграцией с CRM.""",
            price=499.99,
            token_price=4000,  # Цена в токенах (со скидкой ~20%)
            is_digital=True,
            is_active=True,
            category_id=bots_category.id,
            name_ua="Telegram бот для бізнесу",
            name_en="Telegram Bot for Business",
            name_de="Telegram-Bot für Unternehmen",
            name_ru="Telegram бот для бизнеса",
            description_ua="""Повнофункціональний Telegram бот для вашого бізнесу з можливостями 
                прийому замовлень, обробки платежів та інтеграцією з CRM.""",
            description_en="""Full-featured Telegram bot for your business with capabilities for 
                order processing, payment processing, and CRM integration.""",
            description_de="""Voll funktionsfähiger Telegram-Bot für Ihr Unternehmen mit Funktionen zur 
                Auftragsabwicklung, Zahlungsabwicklung und CRM-Integration.""",
            description_ru="""Полнофункциональный Telegram бот для вашего бизнеса с возможностями 
                приема заказов, обработки платежей и интеграцией с CRM."""
        ),
        Product(
            name="Discord бот для сообщества",
            slug="discord-bot-community",
            description="""Discord бот для управления вашим сообществом, модерации чатов,
                проведения мероприятий и аналитики активности пользователей.""",
            price=399.99,
            token_price=3200,
            is_digital=True,
            is_active=True,
            category_id=bots_category.id,
            name_ua="Discord бот для спільноти",
            name_en="Discord Bot for Community",
            name_de="Discord-Bot für Community",
            name_ru="Discord бот для сообщества",
            description_ua="""Discord бот для управління вашою спільнотою, модерації чатів,
                проведення заходів та аналітики активності користувачів.""",
            description_en="""Discord bot for managing your community, chat moderation,
                hosting events and user activity analytics.""",
            description_de="""Discord-Bot zur Verwaltung Ihrer Community, Chat-Moderation,
                Veranstaltungen und Benutzeraktivitätsanalysen.""",
            description_ru="""Discord бот для управления вашим сообществом, модерации чатов,
                проведения мероприятий и аналитики активности пользователей."""
        ),
        Product(
            name="Корпоративный сайт",
            slug="corporate-website",
            description="""Современный корпоративный сайт с адаптивным дизайном, системой управления контентом,
                блогом и интеграцией с социальными сетями.""",
            price=1499.99,
            token_price=12000,
            is_digital=True,
            is_active=True,
            category_id=websites_category.id,
            name_ua="Корпоративний сайт",
            name_en="Corporate Website",
            name_de="Unternehmenswebsite",
            name_ru="Корпоративный сайт",
            description_ua="""Сучасний корпоративний сайт з адаптивним дизайном, системою управління контентом,
                блогом та інтеграцією з соціальними мережами.""",
            description_en="""Modern corporate website with responsive design, content management system,
                blog and social media integration.""",
            description_de="""Moderne Unternehmenswebsite mit responsivem Design, Content-Management-System,
                Blog und Social-Media-Integration.""",
            description_ru="""Современный корпоративный сайт с адаптивным дизайном, системой управления контентом,
                блогом и интеграцией с социальными сетями."""
        ),
        Product(
            name="Интернет-магазин",
            slug="e-commerce-website",
            description="""Полнофункциональный интернет-магазин с каталогом товаров, корзиной,
                системой онлайн-оплаты и панелью администратора.""",
            price=2499.99,
            token_price=20000,
            is_digital=True,
            is_active=True,
            category_id=websites_category.id,
            name_ua="Інтернет-магазин",
            name_en="E-commerce Website",
            name_de="E-Commerce-Website",
            name_ru="Интернет-магазин",
            description_ua="""Повнофункціональний інтернет-магазин з каталогом товарів, кошиком,
                системою онлайн-оплати та панеллю адміністратора.""",
            description_en="""Full-featured e-commerce website with product catalog, shopping cart,
                online payment system and admin panel.""",
            description_de="""Voll funktionsfähige E-Commerce-Website mit Produktkatalog, Warenkorb,
                Online-Zahlungssystem und Adminpanel.""",
            description_ru="""Полнофункциональный интернет-магазин с каталогом товаров, корзиной,
                системой онлайн-оплаты и панелью администратора."""
        ),
        Product(
            name="Мобильное приложение iOS",
            slug="ios-app",
            description="""Разработка нативного мобильного приложения для iOS с дизайном,
                соответствующим стандартам Apple, и публикацией в App Store.""",
            price=3999.99,
            token_price=32000,
            is_digital=True,
            is_active=True,
            category_id=apps_category.id,
            name_ua="Мобільний додаток iOS",
            name_en="iOS Mobile App",
            name_de="iOS Mobile App",
            name_ru="Мобильное приложение iOS",
            description_ua="""Розробка нативного мобільного додатку для iOS з дизайном,
                відповідним стандартам Apple, і публікацією в App Store.""",
            description_en="""Development of native mobile application for iOS with design
                according to Apple standards and publishing in the App Store.""",
            description_de="""Entwicklung einer nativen mobilen Anwendung für iOS mit Design
                gemäß Apple-Standards und Veröffentlichung im App Store.""",
            description_ru="""Разработка нативного мобильного приложения для iOS с дизайном,
                соответствующим стандартам Apple, и публикацией в App Store."""
        ),
        Product(
            name="Мобильное приложение Android",
            slug="android-app",
            description="""Разработка нативного мобильного приложения для Android с дизайном,
                соответствующим стандартам Material Design, и публикацией в Google Play.""",
            price=3499.99,
            token_price=28000,
            is_digital=True,
            is_active=True,
            category_id=apps_category.id,
            name_ua="Мобільний додаток Android",
            name_en="Android Mobile App",
            name_de="Android Mobile App",
            name_ru="Мобильное приложение Android",
            description_ua="""Розробка нативного мобільного додатку для Android з дизайном,
                відповідним стандартам Material Design, і публікацією в Google Play.""",
            description_en="""Development of native mobile application for Android with design
                according to Material Design standards and publishing in Google Play.""",
            description_de="""Entwicklung einer nativen mobilen Anwendung für Android mit Design
                gemäß Material Design-Standards und Veröffentlichung in Google Play.""",
            description_ru="""Разработка нативного мобильного приложения для Android с дизайном,
                соответствующим стандартам Material Design, и публикацией в Google Play."""
        ),    ]
    
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    
    # Создаем блоки контента для главной страницы
    blocks = [
        Block(
            title="Аирдроп ITST токенов",
            title_ua="Аірдроп ITST токенів",
            title_en="ITST Token Airdrop",
            title_de="ITST Token Airdrop",
            title_ru="Аирдроп ITST токенов",
            content="Получите бесплатные токены ITST, участвуя в нашем аирдропе!",
            content_ua="Отримайте безкоштовні токени ITST, беручи участь у нашому аірдропі!",
            content_en="Get free ITST tokens by participating in our airdrop!",
            content_de="Erhalten Sie kostenlose ITST-Token durch die Teilnahme an unserem Airdrop!",
            content_ru="Получите бесплатные токены ITST, участвуя в нашем аирдропе!",
            order=1,
            is_active=True,
            slug="airdrop",
            is_top=False
        ),
        Block(
            title="Токенсейл ITST",
            title_ua="Токенсейл ITST",
            title_en="ITST Token Sale",
            title_de="ITST Token-Verkauf",
            title_ru="Токенсейл ITST",
            content="Купите токены ITST по специальной цене во время токенсейла!",
            content_ua="Купуйте токени ITST за спеціальною ціною під час токенсейлу!",
            content_en="Buy ITST tokens at a special price during the token sale!",
            content_de="Kaufen Sie ITST-Token zu einem Sonderpreis während des Token-Verkaufs!",
            content_ru="Купите токены ITST по специальной цене во время токенсейла!",
            order=2,
            is_active=True,
            slug="tokensale",
            is_top=False
        ),
        Block(
            title="DAO управление",
            title_ua="DAO управління",
            title_en="DAO Governance",
            title_de="DAO-Verwaltung",
            title_ru="DAO управление",
            content="Участвуйте в управлении проектом через децентрализованную автономную организацию!",
            content_ua="Беріть участь в управлінні проектом через децентралізовану автономну організацію!",
            content_en="Participate in project governance through a decentralized autonomous organization!",
            content_de="Beteiligen Sie sich an der Projektführung durch eine dezentrale autonome Organisation!",
            content_ru="Участвуйте в управлении проектом через децентрализованную автономную организацию!",
            order=3,
            is_active=True,
            slug="dao",
            is_top=False
        ),
        Block(
            title="Telegram боты",
            title_ua="Telegram боти",
            title_en="Telegram Bots",
            title_de="Telegram-Bots",
            title_ru="Telegram боты",
            content="Автоматизируйте ваш бизнес с помощью наших Telegram ботов!",
            content_ua="Автоматизуйте ваш бізнес за допомогою наших Telegram ботів!",
            content_en="Automate your business with our Telegram bots!",
            content_de="Automatisieren Sie Ihr Geschäft mit unseren Telegram-Bots!",
            content_ru="Автоматизируйте ваш бизнес с помощью наших Telegram ботов!",
            order=4,
            is_active=True,
            slug="bots",
            is_top=False
        ),
        Block(
            title="Разработка сайтов",
            title_ua="Розробка сайтів",
            title_en="Website Development",
            title_de="Website-Entwicklung",
            title_ru="Разработка сайтов",
            content="Создаем современные веб-сайты любой сложности!",
            content_ua="Створюємо сучасні веб-сайти будь-якої складності!",
            content_en="We create modern websites of any complexity!",
            content_de="Wir erstellen moderne Websites jeder Komplexität!",
            content_ru="Создаем современные веб-сайты любой сложности!",
            order=5,
            is_active=True,
            slug="websites",
            is_top=False
        ),
        Block(
            title="IT Shop токен",
            title_ua="IT Shop токен",
            title_en="IT Shop Token",
            title_de="IT Shop Token",
            title_ru="IT Shop токен",
            content="Узнайте больше о нашем токене ITST и его возможностях!",
            content_ua="Дізнайтеся більше про наш токен ITST та його можливості!",
            content_en="Learn more about our ITST token and its capabilities!",
            content_de="Erfahren Sie mehr über unser ITST-Token und seine Möglichkeiten!",
            content_ru="Узнайте больше о нашем токене ITST и его возможностях!",
            order=0,
            is_active=True,
            slug="main",
            is_top=True
        )
    ]
    
    for block in blocks:
        db.session.add(block)
    
    db.session.commit()
    
    # Создаем администратора, если его нет
    admin_username = "Andrii"
    admin_password = "Dnepr75ok10"
    admin = User.query.filter_by(username=admin_username).first()
    if not admin:
        admin = User(
            username=admin_username,
            password_hash=generate_password_hash(admin_password),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print(f"Админ-пользователь '{admin_username}' создан!")
    else:
        print(f"Админ-пользователь '{admin_username}' уже существует.")
    
    print("Демоданные успешно созданы!")

if __name__ == "__main__":
    # Для тестирования
    create_demo_data()
