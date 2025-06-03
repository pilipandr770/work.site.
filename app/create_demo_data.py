#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для создания демо-данных в базе данных.
Запускать после migrations_update.py
"""

from app import create_app
from app.utils.demo_data import create_demo_data

def run_create_demo_data():
    """Запускает создание демо-данных внутри контекста приложения"""
    app = create_app()
    with app.app_context():
        create_demo_data()

if __name__ == "__main__":
    run_create_demo_data()
