# app/blockchain/__init__.py
from flask import Blueprint

blockchain = Blueprint('blockchain', __name__)

from app.blockchain import routes
