#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для создания и обновления таблиц базы данных.
Этот скрипт нужно запустить перед первым запуском приложения, 
а также после любых изменений в моделях.
"""

from app import create_app, db
from app.models import User, Block, Settings, Token, Airdrop, TokenSale, DaoProposal
from app.models import Category, Product, Cart, CartItem, Order, OrderItem
from app.models import AirdropParticipation, TokenPurchase, DaoVote
from werkzeug.security import generate_password_hash

def create_admin():
    """Создает администратора, если его нет"""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("Создан администратор с логином 'admin' и паролем 'admin'")
    else:
        print("Администратор уже существует")

def run_migrations():
    """Создает или обновляет таблицы базы данных"""
    print("Создание/обновление таблиц базы данных...")
    app = create_app()
    with app.app_context():
        # Создание таблиц
        db.create_all()
        # Создание админа
        create_admin()
        print("База данных успешно обновлена!")

if __name__ == "__main__":
    run_migrations()
