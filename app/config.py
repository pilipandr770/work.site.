# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LANGUAGES = ['uk', 'en', 'ru']
    UPLOAD_FOLDER = 'app/static/uploads'
    TOKEN_CONTRACT_ADDRESS = os.environ.get('TOKEN_CONTRACT_ADDRESS')
    TOKEN_RECEIVER_ADDRESS = os.environ.get('TOKEN_RECEIVER_ADDRESS')
