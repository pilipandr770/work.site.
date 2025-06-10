import sys
import os
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('blog_debug')

# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models import BlogPost, User
from werkzeug.security import generate_password_hash
import json
import traceback
from datetime import datetime

def ensure_test_admin_exists(app):
    """Убедимся, что в базе данных есть тестовый админ"""
    with app.app_context():
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            logger.info("Создаем тестового админа...")
            admin = User(
                username='admin',
                password_hash=generate_password_hash('adminpassword'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            logger.info(f"Тестовый админ создан с ID: {admin.id}")
        else:
            logger.info(f"Тестовый админ уже существует (ID: {admin.id})")
        return admin

def debug_database_operations():
    """Проверяем операции с базой данных напрямую"""
    logger.info("=== ОТЛАДКА ОПЕРАЦИЙ С БАЗОЙ ДАННЫХ ===")
    
    app = create_app()
    
    # Проверка создания поста
    with app.app_context():
        try:
            logger.info("Пробуем создать пост напрямую через модель...")
            
            # Поиск поста по слагу для проверки
            test_slug = "test-direct-model-post"
            existing_post = BlogPost.query.filter_by(slug=test_slug).first()
            
            if existing_post:
                logger.info(f"Пост с slug '{test_slug}' уже существует (ID: {existing_post.id})")
                logger.info("Удаляем существующий пост для чистого теста...")
                db.session.delete(existing_post)
                db.session.commit()
            
            # Создаем новый пост
            post = BlogPost(
                title="Тестовый пост через модель напрямую",
                slug=test_slug,
                content="Содержимое тестового поста через модель напрямую",
                summary="Краткое описание для отладки модели",
                is_published=True,
                publish_date=datetime.utcnow()
            )
            
            logger.info("Добавляем пост в сессию...")
            db.session.add(post)
            
            logger.info("Коммитим изменения...")
            db.session.commit()
            logger.info(f"Пост успешно сохранен с ID: {post.id}")
            
            # Верифицируем, что пост был сохранен
            saved_post = BlogPost.query.filter_by(slug=test_slug).first()
            if saved_post:
                logger.info("Верификация: пост найден в базе данных:")
                logger.info(f"ID: {saved_post.id}")
                logger.info(f"Title: {saved_post.title}")
                logger.info(f"Is Published: {saved_post.is_published}")
            else:
                logger.error("Критическая ошибка: пост не найден в базе данных после сохранения!")
        
        except Exception as e:
            logger.error(f"Ошибка при создании поста: {str(e)}")
            logger.error(traceback.format_exc())
            db.session.rollback()

def debug_session_objects():
    """Проверяем состояние сессий базы данных"""
    logger.info("=== ОТЛАДКА СОСТОЯНИЯ СЕССИЙ БД ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            # Проверяем состояние сессии
            logger.info(f"Текущая сессия: {db.session}")
            logger.info(f"Автоматический коммит: {db.session.autocommit}")
            logger.info(f"Автоматический флаш: {db.session.autoflush}")
            
            # Проверяем соединение с базой данных
            result = db.session.execute("SELECT 1").scalar()
            logger.info(f"Проверка соединения с БД: {result}")
            
            # Получаем информацию о таблице BlogPost
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = inspector.get_columns('blog_post')
            logger.info(f"Столбцы таблицы blog_post: {[c['name'] for c in columns]}")
            
        except Exception as e:
            logger.error(f"Ошибка при отладке сессий: {str(e)}")
            logger.error(traceback.format_exc())

def check_all_blog_posts():
    """Проверяем все записи в таблице BlogPost"""
    logger.info("=== ПРОВЕРКА ВСЕХ ЗАПИСЕЙ В ТАБЛИЦЕ BLOG_POST ===")
    
    app = create_app()
    
    with app.app_context():
        try:
            posts = BlogPost.query.all()
            logger.info(f"Всего постов в БД: {len(posts)}")
            
            for post in posts:
                logger.info(f"ID: {post.id}")
                logger.info(f"Title: {post.title}")
                logger.info(f"Slug: {post.slug}")
                logger.info(f"Published: {post.is_published}")
                logger.info(f"Publish Date: {post.publish_date}")
                logger.info(f"Created At: {post.created_at}")
                logger.info("---")
                
        except Exception as e:
            logger.error(f"Ошибка при проверке постов: {str(e)}")
            logger.error(traceback.format_exc())

if __name__ == "__main__":
    logger.info("Начинаем отладку базы данных...")
    debug_database_operations()
    debug_session_objects()
    check_all_blog_posts()
    logger.info("Отладка завершена!")
