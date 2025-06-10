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
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash
from app.forms import BlogPostForm
from flask import url_for
import flask

def setup_test_app():
    """Создает тестовое приложение с расширенным логированием"""
    app = create_app()
    
    # Включаем детальное логирование запросов Flask
    app.config['DEBUG'] = True
    
    # Перехватываем запросы и ответы для отладки
    @app.before_request
    def log_request_info():
        logger.debug('Headers: %s', flask.request.headers)
        logger.debug('Body: %s', flask.request.get_data())
        logger.debug('Form: %s', flask.request.form)
        logger.debug('Files: %s', flask.request.files)

    @app.after_request
    def log_response_info(response):
        logger.debug('Response Status: %s', response.status)
        logger.debug('Response Headers: %s', response.headers)
        return response
    
    return app

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

def simulate_admin_login(app, admin_user):
    """Симулируем вход админа в систему"""
    with app.test_request_context():
        logger.info("Логин тестового админа...")
        login_user(admin_user)
        logger.info(f"Текущий пользователь: {current_user.username if current_user.is_authenticated else 'Not authenticated'}")

def debug_form_validation():
    """Отлаживаем валидацию формы BlogPostForm"""
    logger.info("=== ОТЛАДКА ВАЛИДАЦИИ ФОРМЫ ===")
    
    app = setup_test_app()
    with app.app_context():
        form = BlogPostForm(
            title="Тестовый пост для отладки",
            slug="test-debug-post",
            content="Содержимое тестового поста для отладки",
            summary="Краткое описание для отладки",
            is_published=True
        )
        
        logger.info(f"Валидная форма? {form.validate()}")
        if not form.validate():
            for field, errors in form.errors.items():
                logger.error(f"Поле {field}: {', '.join(errors)}")
        else:
            logger.info("Форма прошла валидацию успешно!")

def debug_admin_interface():
    """Отлаживаем интерфейс админа для блога"""
    logger.info("=== ОТЛАДКА АДМИНСКОГО ИНТЕРФЕЙСА ===")
    
    app = setup_test_app()
    admin = ensure_test_admin_exists(app)
    
    # Проверяем доступ к URL админки
    with app.test_client() as client:
        # Логинимся как админ
        with client.session_transaction() as session:
            session['user_id'] = admin.id
        
        # Проверяем доступ к списку постов
        response = client.get('/blog/admin/posts')
        logger.info(f"GET /blog/admin/posts - Статус: {response.status_code}")
        
        # Проверяем доступ к странице создания поста
        response = client.get('/blog/admin/posts/create')
        logger.info(f"GET /blog/admin/posts/create - Статус: {response.status_code}")
        
        # Пробуем создать пост
        post_data = {
            'title': 'Тестовый пост через клиент',
            'slug': 'test-client-post',
            'content': 'Содержимое тестового поста через клиент',
            'summary': 'Краткое описание',
            'is_published': True
        }
        
        logger.info("Пытаемся создать пост через POST запрос...")
        response = client.post('/blog/admin/posts/create', 
                              data=post_data,
                              follow_redirects=True)
        
        logger.info(f"POST /blog/admin/posts/create - Статус: {response.status_code}")
        logger.info(f"Ответ: {response.data.decode('utf-8')[:200]}...")
        
        # Проверяем, был ли создан пост
        with app.app_context():
            post = BlogPost.query.filter_by(slug='test-client-post').first()
            if post:
                logger.info(f"Пост успешно создан с ID: {post.id}")
            else:
                logger.error("Пост НЕ был создан в базе данных!")

def check_database_commit_hooks():
    """Проверяем перехватчики событий базы данных, которые могут влиять на сохранение"""
    logger.info("=== ПРОВЕРКА ПЕРЕХВАТЧИКОВ БД ===")
    
    app = create_app()
    with app.app_context():
        # Проверяем события SQLAlchemy
        logger.info("Проверяем события SQLAlchemy...")
        for listener in db.event.registry._key_to_collection:
            logger.info(f"Listener: {listener}")

if __name__ == "__main__":
    logger.info("Начинаем отладку админского интерфейса блога...")
    debug_form_validation()
    debug_admin_interface()
    check_database_commit_hooks()
    logger.info("Отладка завершена!")
