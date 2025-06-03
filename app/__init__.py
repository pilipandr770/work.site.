# app/__init__.py
import os
from flask import Flask, g, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel
from pathlib import Path

# Загрузка переменных из .env файла
try:
    from dotenv import load_dotenv
    # Попытка загрузки .env файла из корневой директории проекта
    env_path = Path(__file__).resolve().parent.parent / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Переменные окружения загружены из {env_path}")
except ImportError:
    print("python-dotenv не установлен, переменные окружения должны быть настроены вручную")

db = SQLAlchemy()
login_manager = LoginManager()
babel = Babel()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    login_manager.login_message = 'Будь ласка, увійдіть в систему для доступу до цієї сторінки.'
    babel.init_app(app)
    
    # Create database tables if they don't exist
    from .models import Block  # Import Block to ensure it's registered with SQLAlchemy
    with app.app_context():
        db.create_all()
        print("Database tables created with db.create_all()")

    # Зберігати вибір мови в сесії
    @app.before_request
    def set_lang():
        lang = request.args.get('lang')
        if lang:
            session['lang'] = lang
        g.lang = session.get('lang', None)
    
    # Підключення blueprint'ів
    from app.main.routes import main
    from app.admin.routes import admin
    from app.shop.routes import shop
    from app.blockchain.routes import blockchain
    from .assist import assist_bp
    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(shop)
    app.register_blueprint(blockchain)
    app.register_blueprint(assist_bp)

    # Регистрируем template helper функции как глобальные в Jinja2
    from app.main.routes import (
        get_block_title, get_block_content, get_category_name, get_product_name, 
        get_product_description, get_token_description, get_airdrop_title, 
        get_airdrop_description, get_token_sale_title, get_token_sale_description,
        get_dao_proposal_title, get_dao_proposal_description
    )
    
    app.jinja_env.globals.update(
        get_block_title=get_block_title,
        get_block_content=get_block_content,
        get_category_name=get_category_name,
        get_product_name=get_product_name,
        get_product_description=get_product_description,
        get_token_description=get_token_description,
        get_airdrop_title=get_airdrop_title,
        get_airdrop_description=get_airdrop_description,
        get_token_sale_title=get_token_sale_title,
        get_token_sale_description=get_token_sale_description,
        get_dao_proposal_title=get_dao_proposal_title,
        get_dao_proposal_description=get_dao_proposal_description
    )

    return app

# Babel локалізатор
@babel.localeselector
def get_locale():
    from flask import request, session
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
        return lang
    if 'lang' in session:
        return session['lang']
    return request.accept_languages.best_match(['uk', 'en', 'de', 'ru'])

from app.models import User

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    """Повертає користувача для Flask-Login за id"""
    return User.query.get(int(user_id))
