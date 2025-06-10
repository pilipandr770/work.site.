"""
Blog automation module to generate and schedule blog content using AI
"""
from flask import Blueprint

# Create Blueprint for blog automation module
blog_automation_bp = Blueprint('blog_automation', __name__, url_prefix='/admin/blog-automation')

# Import routes after Blueprint initialization to avoid circular imports
from app.blog_automation import routes
