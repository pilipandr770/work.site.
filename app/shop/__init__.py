# app/shop/__init__.py
from flask import Blueprint

shop = Blueprint('shop', __name__)

from app.shop import routes
