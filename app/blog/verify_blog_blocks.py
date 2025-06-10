# app/blog/verify_blog_blocks.py
# Скрипт для проверки работы упрощенной системы блогов с 12 блоками

from app import create_app, db
from app.models import BlogBlock
from datetime import datetime
import sys

app = create_app()
with app.app_context():
    print("== Проверка базы данных блогов ==")
    
    # Подсчет блоков
    blocks_count = BlogBlock.query.count()
    print(f"Количество блоков в базе данных: {blocks_count}")
    
    # Проверяем наличие всех 12 блоков
    missing = []
    for position in range(1, 13):
        block = BlogBlock.query.filter_by(position=position).first()
        if not block:
            missing.append(position)
            
    if missing:
        print(f"ВНИМАНИЕ: Отсутствуют блоки для позиций: {', '.join(map(str, missing))}")
        print("Запустите административную панель для автоматического создания недостающих блоков.")
    else:
        print("OK: Все 12 блоков найдены в базе данных.")
    
    # Проверяем активные блоки
    active_blocks = BlogBlock.query.filter_by(is_active=True).count()
    print(f"Активных блоков: {active_blocks}")
    
    # Выводим информацию о всех блоках
    print("\n== Информация о блоках ==")
    print("-" * 80)
    print(f"{'ID':4} | {'Поз':3} | {'Активн':6} | {'Заголовок':<40} | {'Картинка':<15}")
    print("-" * 80)
    
    for block in BlogBlock.query.order_by(BlogBlock.position).all():
        status = "Да" if block.is_active else "Нет"
        title = block.title[:37] + "..." if len(block.title or "") > 40 else (block.title or "")
        image = block.featured_image or "-"
        if len(image) > 15:
            image = image[:12] + "..."
        
        print(f"{block.id:4} | {block.position:3} | {status:6} | {title:<40} | {image:<15}")
    
    print("\nПроверка завершена.")
