"""
Models for blog automation system
"""
from datetime import datetime
from app.models import db

class BlogTopic(db.Model):
    """Topics for blog content generation"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_for = db.Column(db.DateTime, nullable=True)
    
    # References the generated blog block (if any)
    blog_block_id = db.Column(db.Integer, db.ForeignKey('blog_block.id'), nullable=True)
    blog_block = db.relationship('BlogBlock', backref='generated_from_topic', lazy=True)
    
    def __repr__(self):
        return f'<BlogTopic {self.title}>'

class AutopostingSchedule(db.Model):
    """Schedule configuration for automated blog posting"""
    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=False)
    days_of_week = db.Column(db.String(20), default='0,1,2,3,4,5,6')  # CSV of days (0=Monday, 6=Sunday)
    posting_time = db.Column(db.String(5), default='12:00')  # HH:MM format
    
    # Translation settings
    auto_translate = db.Column(db.Boolean, default=True)
    target_languages = db.Column(db.String(50), default='en,de,ru')  # CSV of language codes
    
    # Image generation settings
    generate_images = db.Column(db.Boolean, default=True)
    image_style = db.Column(db.String(100), default='professional, high quality')
    
    # Social media settings
    post_to_telegram = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<AutopostingSchedule {self.id}>'

class ContentGenerationLog(db.Model):
    """Log of content generation activities"""
    id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('blog_topic.id', ondelete='SET NULL'), nullable=True)
    topic = db.relationship('BlogTopic', backref='logs', lazy=True)
    
    action = db.Column(db.String(50), nullable=False)  # generate_content, translate, generate_image, post_telegram
    status = db.Column(db.String(20), default='success')  # success, failed
    message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Add duration tracking for performance analysis
    duration_seconds = db.Column(db.Float, nullable=True)
    
    def __repr__(self):
        return f'<ContentGenerationLog {self.action} - {self.status}>'
        
    @classmethod
    def add_log(cls, topic=None, action="", status="success", message="", duration_seconds=None):
        """Helper method to quickly add a log entry"""
        try:
            log = cls(
                topic_id=topic.id if topic else None,
                action=action,
                status=status,
                message=message,
                duration_seconds=duration_seconds
            )
            db.session.add(log)
            db.session.commit()
            return log
        except Exception as e:
            # Failsafe logging in case of database errors
            import logging
            logging.getLogger(__name__).error(f"Error logging activity: {str(e)}")
            return None
