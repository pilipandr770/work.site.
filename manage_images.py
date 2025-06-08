#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Утилита для управления изображениями
"""

import os
import shutil
from datetime import datetime
from app import create_app, db
from app.models import Block, Product, Category, PaymentMethod, ProductImage

def check_missing_images():
    """Проверяет отсутствующие изображения в БД"""
    app = create_app()
    
    with app.app_context():
        print("🔍 ПРОВЕРКА ОТСУТСТВУЮЩИХ ИЗОБРАЖЕНИЙ\n")
        
        uploads_path = os.path.join('app', 'static', 'uploads')
        missing_files = []
        
        # Проверяем блоки
        blocks = Block.query.filter(Block.image.isnot(None)).all()
        print(f"📋 Блоки с изображениями: {len(blocks)}")
        for block in blocks:
            file_path = os.path.join(uploads_path, block.image)
            if not os.path.exists(file_path):
                print(f"❌ Блок '{block.title}': файл {block.image} не найден")
                missing_files.append(('block', block.id, block.image))
            else:
                print(f"✅ Блок '{block.title}': {block.image}")
        
        # Проверяем продукты
        products = Product.query.filter(Product.image.isnot(None)).all()
        print(f"\n🛍️ Продукты с изображениями: {len(products)}")
        for product in products:
            file_path = os.path.join(uploads_path, product.image)
            if not os.path.exists(file_path):
                print(f"❌ Продукт '{product.name}': файл {product.image} не найден")
                missing_files.append(('product', product.id, product.image))
            else:
                print(f"✅ Продукт '{product.name}': {product.image}")
        
        # Проверяем дополнительные изображения продуктов
        product_images = ProductImage.query.all()
        print(f"\n🖼️ Дополнительные изображения продуктов: {len(product_images)}")
        for img in product_images:
            file_path = os.path.join(uploads_path, img.image_path)
            if not os.path.exists(file_path):
                print(f"❌ Изображение продукта: файл {img.image_path} не найден")
                missing_files.append(('product_image', img.id, img.image_path))
            else:
                print(f"✅ Изображение продукта: {img.image_path}")
        
        # Проверяем категории
        categories = Category.query.filter(Category.image.isnot(None)).all()
        print(f"\n📂 Категории с изображениями: {len(categories)}")
        for category in categories:
            file_path = os.path.join(uploads_path, category.image)
            if not os.path.exists(file_path):
                print(f"❌ Категория '{category.name}': файл {category.image} не найден")
                missing_files.append(('category', category.id, category.image))
            else:
                print(f"✅ Категория '{category.name}': {category.image}")
        
        # Проверяем платежные методы
        payment_methods = PaymentMethod.query.filter(PaymentMethod.qr_code.isnot(None)).all()
        print(f"\n💳 Платежные методы с QR-кодами: {len(payment_methods)}")
        for method in payment_methods:
            file_path = os.path.join(uploads_path, method.qr_code)
            if not os.path.exists(file_path):
                print(f"❌ Платежный метод '{method.name}': файл {method.qr_code} не найден")
                missing_files.append(('payment_method', method.id, method.qr_code))
            else:
                print(f"✅ Платежный метод '{method.name}': {method.qr_code}")
        
        print(f"\n📊 ИТОГО:")
        print(f"Всего отсутствующих файлов: {len(missing_files)}")
        
        return missing_files

def list_upload_files():
    """Показывает все файлы в папке uploads"""
    uploads_path = os.path.join('app', 'static', 'uploads')
    
    print("📁 ФАЙЛЫ В ПАПКЕ UPLOADS:\n")
    
    if not os.path.exists(uploads_path):
        print("❌ Папка uploads не существует!")
        return
    
    files = os.listdir(uploads_path)
    files = [f for f in files if not f.startswith('.')]
    
    if not files:
        print("📭 Папка uploads пуста")
        return
    
    for file in sorted(files):
        file_path = os.path.join(uploads_path, file)
        size = os.path.getsize(file_path)
        size_mb = size / (1024 * 1024)
        print(f"📄 {file} ({size_mb:.2f} MB)")
    
    print(f"\nВсего файлов: {len(files)}")

def backup_uploads():
    """Создает резервную копию папки uploads"""
    uploads_path = os.path.join('app', 'static', 'uploads')
    
    if not os.path.exists(uploads_path):
        print("❌ Папка uploads не существует!")
        return
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"uploads_backup_{timestamp}"
    
    shutil.copytree(uploads_path, backup_path)
    print(f"✅ Резервная копия создана: {backup_path}")

def show_gitignore_status():
    """Показывает статус .gitignore для папки uploads"""
    print("📝 СТАТУС .GITIGNORE:\n")
    
    with open('.gitignore', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    upload_lines = [i for i, line in enumerate(lines) if 'uploads' in line.lower()]
    
    for i in upload_lines:
        line = lines[i].strip()
        if line.startswith('#'):
            print(f"💬 {line}")
        elif 'uploads/*' in line:
            print(f"🚫 {line} (изображения игнорируются)")
        elif 'uploads' in line:
            print(f"📁 {line}")

if __name__ == "__main__":
    print("🖼️ УТИЛИТА УПРАВЛЕНИЯ ИЗОБРАЖЕНИЯМИ\n")
    
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'check':
            check_missing_images()
        elif command == 'list':
            list_upload_files()
        elif command == 'backup':
            backup_uploads()
        elif command == 'gitignore':
            show_gitignore_status()
        else:
            print("❌ Неизвестная команда")
    else:
        print("🔧 Доступные команды:")
        print("  python manage_images.py check     - проверить отсутствующие изображения")
        print("  python manage_images.py list      - показать все файлы")
        print("  python manage_images.py backup    - создать резервную копию")
        print("  python manage_images.py gitignore - показать статус .gitignore")
        print()
        
        # Запускаем быструю проверку
        list_upload_files()
        print("\n" + "="*50 + "\n")
        check_missing_images()
        print("\n" + "="*50 + "\n")
        show_gitignore_status()
