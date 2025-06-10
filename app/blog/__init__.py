# app/blog/__init__.py
from flask import Blueprint

blog_bp = Blueprint('blog', __name__)

# Импортируем маршруты блога
from . import routes
