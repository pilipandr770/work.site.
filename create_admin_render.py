#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Создание администратора для Render.com
Этот скрипт создает администратора в базе данных, если он еще не существует.
Запустите его вручную на Render.com или добавьте в prestart.sh.
"""

import os
import sys

def create_admin_for_render():
    """
    Создает администратора, если он не существует
    """
    print("=" * 60)
    print("СОЗДАНИЕ АДМИНИСТРАТОРА НА RENDER")
    print("=" * 60)

    try:
        from app import create_app, db
        from app.models import User
        from werkzeug.security import generate_password_hash
        
        # Задайте имя пользователя и пароль
        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'andrii770')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Dnepr75ok6137707')
        
        print(f"Проверяем существование администратора '{ADMIN_USERNAME}'...")
        
        # Создаем приложение и контекст
        app = create_app()
        with app.app_context():
            # Проверяем, существует ли уже администратор
            if not User.query.filter_by(username=ADMIN_USERNAME).first():
                # Хешируем пароль и создаем пользователя
                hashed_password = generate_password_hash(ADMIN_PASSWORD)
                user = User(username=ADMIN_USERNAME, password_hash=hashed_password)
                db.session.add(user)
                db.session.commit()
                print(f"✅ Администратор '{ADMIN_USERNAME}' успешно создан!")
            else:
                print(f"⚠️ Администратор '{ADMIN_USERNAME}' уже существует.")

        return True
    except Exception as e:
        print(f"❌ Ошибка при создании администратора: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_admin_for_render()
    sys.exit(0 if success else 1)
