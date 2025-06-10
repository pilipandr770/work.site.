# app/utils/filters.py

import markdown
import bleach
from markupsafe import Markup

def register_filters(app):
    """Register custom Jinja2 filters"""
    
    @app.template_filter('markdown')
    def markdown_filter(text):
        """
        Convert markdown text to HTML and safely sanitize it
        
        Usage in templates:
        {{ blog_post.content|markdown|safe }}
        """
        if not text:
            return ""
        
        # Allowed tags and attributes for secure rendering
        allowed_tags = [
            'p', 'br', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'strong', 'em', 'b', 'i', 'u', 'a', 'ul', 'ol', 'li',
            'blockquote', 'code', 'pre', 'hr', 'img', 'table', 'thead',
            'tbody', 'tr', 'th', 'td'
        ]
        
        allowed_attrs = {
            'a': ['href', 'title', 'target', 'rel'],
            'img': ['src', 'alt', 'title', 'width', 'height', 'class'],
            '*': ['class', 'id']
        }
        
        # Convert markdown to HTML
        html = markdown.markdown(
            text,
            extensions=['extra', 'smarty', 'tables', 'codehilite', 'fenced_code']
        )
        
        # Clean and sanitize the HTML
        clean_html = bleach.clean(
            html,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        
    # Mark the result as safe to avoid double-escaping in Jinja
        return Markup(clean_html)
        
    @app.template_filter('nl2br')
    def nl2br_filter(text):
        """
        Convert newlines to <br> tags
        
        Usage in templates:
        {{ log_message|nl2br|safe }}
        """
        if not text:
            return ""
        
        # Replace newlines with <br> tags
        html = text.replace('\n', '<br>')
        
        # Mark the result as safe to avoid double-escaping in Jinja
        return Markup(html)
