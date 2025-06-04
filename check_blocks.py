from app import create_app, db
from app.models import Block

app = create_app()
with app.app_context():
    blocks = Block.query.all()
    print(f"Найдено блоков: {len(blocks)}")
    
    if blocks:
        print("\nСуществующие блоки:")
        for block in blocks:
            print(f"ID: {block.id}, Заголовок: {block.title}, Slug: {block.slug}, Активен: {block.is_active}")
    else:
        print("В базе данных нет блоков.")
