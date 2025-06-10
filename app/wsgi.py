#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Файл для продакшн-запуска додатку через Gunicorn WSGI-сервер.
"""

from app import create_app

app = create_app()

# Ensure the blog automation scheduler starts in production mode
with app.app_context():
    try:
        from app.blog_automation.models import AutopostingSchedule
        from app.blog_automation.scheduler import get_scheduler
        
        schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
        if schedule:
            scheduler = get_scheduler(app)
            if scheduler:
                scheduler.start()
                print("Blog automation scheduler started in WSGI mode")
    except Exception as e:
        print(f"Error starting blog automation scheduler in WSGI mode: {str(e)}")

if __name__ == "__main__":
    app.run()
