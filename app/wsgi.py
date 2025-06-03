#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для продакшн-запуска додатку через Gunicorn WSGI-сервер.
"""

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
