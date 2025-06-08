from app import create_app, db
from app.models import Block

app = create_app()
with app.app_context():
    # Проверим существующие блоки
    existing_blocks = Block.query.all()
    print(f"Существующих блоков: {len(existing_blocks)}")
    
    # Создаем основные блоки с правильными полями
    blocks_to_create = [
        {
            'slug': 'main-hero',
            'title': 'Добро пожаловать в Ocean Protocol',
            'title_ru': 'Добро пожаловать в Ocean Protocol',
            'title_en': 'Welcome to Ocean Protocol',
            'title_ua': 'Ласкаво просимо до Ocean Protocol',
            'content': 'Революционная платформа для обмена данными и AI',
            'content_ru': 'Революционная платформа для обмена данными и AI',
            'content_en': 'Revolutionary platform for data exchange and AI',
            'content_ua': 'Революційна платформа для обміну даними та AI',
            'order': 1,
            'is_active': True,
            'is_top': True
        },
        {
            'slug': 'airdrop-section',
            'title': 'Airdrop OCEAN',
            'title_ru': 'Airdrop OCEAN',
            'title_en': 'OCEAN Airdrop',
            'title_ua': 'Airdrop OCEAN',
            'content': 'Получите бесплатные токены OCEAN. Участвуйте в нашем эирдропе!',
            'content_ru': 'Получите бесплатные токены OCEAN. Участвуйте в нашем эирдропе!',
            'content_en': 'Get free OCEAN tokens. Participate in our airdrop!',
            'content_ua': 'Отримайте безкоштовні токени OCEAN. Беріть участь у нашому airdrop!',
            'order': 2,
            'is_active': True,
            'is_top': False
        },
        {
            'slug': 'token-sale',
            'title': 'Продажа токенов',
            'title_ru': 'Продажа токенов',
            'title_en': 'Token Sale',
            'title_ua': 'Продаж токенів',
            'content': 'Приобретите токены OCEAN по выгодной цене',
            'content_ru': 'Приобретите токены OCEAN по выгодной цене',
            'content_en': 'Purchase OCEAN tokens at a great price',
            'content_ua': 'Придбайте токени OCEAN за вигідною ціною',
            'order': 3,
            'is_active': True,
            'is_top': False
        },
        {
            'slug': 'dao-section',
            'title': 'DAO Голосование',
            'title_ru': 'DAO Голосование',
            'title_en': 'DAO Voting',
            'title_ua': 'DAO Голосування',
            'content': 'Участвуйте в управлении протоколом через DAO',
            'content_ru': 'Участвуйте в управлении протоколом через DAO',
            'content_en': 'Participate in protocol governance through DAO',
            'content_ua': 'Беріть участь в управлінні протоколом через DAO',
            'order': 4,
            'is_active': True,
            'is_top': False
        },
        {
            'slug': 'shop-section',
            'title': 'Магазин',
            'title_ru': 'Магазин',
            'title_en': 'Shop',
            'title_ua': 'Магазин',
            'content': 'Покупайте товары за токены OCEAN',
            'content_ru': 'Покупайте товары за токены OCEAN',
            'content_en': 'Buy products with OCEAN tokens',
            'content_ua': 'Купуйте товари за токени OCEAN',
            'order': 5,
            'is_active': True,
            'is_top': False
        }
    ]
    
    for block_data in blocks_to_create:
        existing_block = Block.query.filter_by(slug=block_data['slug']).first()
        if not existing_block:
            block = Block(
                slug=block_data['slug'],
                title=block_data['title'],
                title_ru=block_data['title_ru'],
                title_en=block_data['title_en'],
                title_ua=block_data['title_ua'],
                content=block_data['content'],
                content_ru=block_data['content_ru'],
                content_en=block_data['content_en'],
                content_ua=block_data['content_ua'],
                order=block_data['order'],
                is_active=block_data['is_active'],
                is_top=block_data['is_top']
            )
            db.session.add(block)
            print(f"Создан блок: {block_data['slug']}")
        else:
            print(f"Блок уже существует: {block_data['slug']}")
    
    db.session.commit()
    print("Блоки восстановлены!")
    
    # Проверим результат
    all_blocks = Block.query.order_by(Block.order).all()
    print(f"Всего блоков после восстановления: {len(all_blocks)}")
    for block in all_blocks:
        print(f"- {block.slug}: {block.title} (порядок: {block.order}, активен: {block.is_active})")