from app import create_app, db
from app.models import Block

app = create_app()
with app.app_context():
    db.create_all()
    if not Block.query.first():
        # Створюємо 1 головний блок
        top_block = Block(
            title='Головний блок',
            content='Це головний (великий) блок. Додайте тут важливу інформацію.',
            slug='top-block',
            order=1,
            is_active=True,
            is_top=True
        )
        db.session.add(top_block)
        # Створюємо 6 звичайних блоків
        for i in range(1, 7):
            block = Block(
                title=f'Блок {i}',
                content=f'Опис для блоку {i}',
                slug=f'block{i}',
                order=i+1,
                is_active=True,
                is_top=False
            )
            db.session.add(block)
        db.session.commit()
        print('7 блоків створено!')
    else:
        print('Блоки вже існують!')
