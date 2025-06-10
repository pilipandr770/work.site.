# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret')
    
    # Database configuration with PostgreSQL support
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # Fix for Heroku PostgreSQL URL
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Fallback to SQLite for development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['uk', 'en', 'ru']
    UPLOAD_FOLDER = 'app/static/uploads'
    TOKEN_CONTRACT_ADDRESS = os.environ.get('TOKEN_CONTRACT_ADDRESS')
    TOKEN_RECEIVER_ADDRESS = os.environ.get('TOKEN_RECEIVER_ADDRESS')
    
    # OpenAI API settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4')
    
    # Telegram API settings
    TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHANNEL_ID = os.environ.get('TELEGRAM_CHANNEL_ID')
    
    # Blog settings
    BLOG_POSTS_PER_PAGE = int(os.environ.get('BLOG_POSTS_PER_PAGE', 10))
    BLOG_AUTO_PUBLISH = os.environ.get('BLOG_AUTO_PUBLISH', 'False').lower() == 'true'
