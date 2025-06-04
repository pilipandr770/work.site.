from app import create_app, db
from app.models import Block

app = create_app()
with app.app_context():
    # Удаляем тестовый блок (ID: 1)
    test_block = Block.query.get(1)
    if test_block:
        print(f"Удаляем тестовый блок: {test_block.title} (ID: {test_block.id})")
        db.session.delete(test_block)
        db.session.commit()
        print("✅ Тестовый блок успешно удален")
    else:
        print("Тестовый блок не найден")
    
    # Удаляем блок оплат (ID: 7, Slug: payment)
    payment_block = Block.query.filter_by(slug="payment").first()
    if payment_block:
        print(f"Удаляем блок оплат: {payment_block.title} (ID: {payment_block.id})")
        db.session.delete(payment_block)
        db.session.commit()
        print("✅ Блок оплат успешно удален")
    else:
        print("Блок оплат не найден")
    
    # Проверяем оставшиеся блоки
    remaining_blocks = Block.query.order_by(Block.order).all()
    print(f"\nОсталось блоков: {len(remaining_blocks)}")
    print("Оставшиеся блоки:")
    for block in remaining_blocks:
        print(f"ID: {block.id}, Заголовок: {block.title}, Slug: {block.slug}, Активен: {block.is_active}")
