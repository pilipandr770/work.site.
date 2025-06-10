"""
Scheduler for automated blog content generation and posting
"""
import os
import io
import logging
import requests
from datetime import datetime, timedelta
import time
from threading import Thread
from flask import current_app
from werkzeug.utils import secure_filename

from app.models import db, BlogBlock
from app.blog_automation.models import BlogTopic, AutopostingSchedule, ContentGenerationLog
from app.blog_automation.openai_service import OpenAIContentService
from app.blog_automation.telegram_service import TelegramService
from app.utils.file_utils import save_uploaded_file

logger = logging.getLogger(__name__)

class BlogAutomationScheduler:
    """Scheduler for automated blog content generation and posting"""
    
    def __init__(self, app=None):
        self.app = app
        self.openai_service = OpenAIContentService()
        self.telegram_service = TelegramService()
        self._scheduler_thread = None
        self._stop_scheduler = False
    
    def start(self):
        """Start scheduler in background thread"""
        if self._scheduler_thread is None or not self._scheduler_thread.is_alive():
            self._stop_scheduler = False
            self._scheduler_thread = Thread(target=self._run_scheduler)
            self._scheduler_thread.daemon = True
            self._scheduler_thread.start()
            logger.info("Blog automation scheduler started")
            return True
        return False
    
    def stop(self):
        """Stop scheduler thread"""
        if self._scheduler_thread and self._scheduler_thread.is_alive():
            self._stop_scheduler = True
            self._scheduler_thread.join(timeout=5.0)
            logger.info("Blog automation scheduler stopped")
            return True
        return False
    
    def _run_scheduler(self):
        """Main scheduler loop"""
        with self.app.app_context():
            while not self._stop_scheduler:
                try:
                    self._check_scheduled_tasks()
                    time.sleep(60)  # Check every minute
                except Exception as e:
                    logger.error(f"Error in blog automation scheduler: {str(e)}")
                    time.sleep(300)  # If error, wait 5 minutes before retry
    
    def _check_scheduled_tasks(self):
        """Check for tasks that need to be executed"""
        now = datetime.utcnow()
        
        # Get active autoposting schedule
        schedule = AutopostingSchedule.query.filter_by(is_active=True).first()
        if not schedule:
            return
          # Check if it's time to post according to schedule
        current_day = now.weekday()  # 0=Monday, 6=Sunday
        if str(current_day) not in schedule.days_of_week.split(','):
            return
        
        # Safely parse the posting_time string
        try:
            if schedule.posting_time and ':' in schedule.posting_time:
                schedule_hour, schedule_minute = map(int, schedule.posting_time.split(':'))
            else:
                logger.error(f"Invalid posting_time format: {schedule.posting_time}")
                return
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing posting_time: {schedule.posting_time} - {str(e)}")
            return
        
        # Check if it's the right time (within 5 minutes of scheduled time)
        if now.hour == schedule_hour and abs(now.minute - schedule_minute) <= 5:
            # Find pending topic to process
            topic = BlogTopic.query.filter_by(status='pending').order_by(BlogTopic.created_at).first()
            if topic:
                self._process_topic(topic, schedule)
    
    def _process_topic(self, topic, schedule):
        """Process a blog topic - generate content, translate, create image, post"""
        try:
            # Mark as processing
            topic.status = 'processing'
            db.session.commit()
            
            # Generate content
            result = self.openai_service.generate_blog_content(topic.title, topic.description)
            if not result.get('success'):
                self._log_activity(topic, 'generate_content', 'failed', result.get('error'))
                topic.status = 'failed'
                db.session.commit()
                return
            
            content = result.get('content')
            self._log_activity(topic, 'generate_content', 'success', "Content generated successfully")
            
            # Find an available position for the new block
            position = self._get_available_block_position()
            
            # Create blog block with generated content
            blog_block = BlogBlock(
                title=topic.title,
                content=content,
                summary=content[:200] + "..." if len(content) > 200 else content,
                position=position,
                is_active=True
            )
            
            db.session.add(blog_block)
            db.session.commit()
            
            # Link topic to blog block
            topic.blog_block_id = blog_block.id
            db.session.commit()
            
            # Translate content if enabled
            if schedule.auto_translate:
                self._translate_content(blog_block, schedule.target_languages.split(','))
            
            # Generate image if enabled
            if schedule.generate_images:
                self._generate_image(blog_block, topic)
            
            # Post to Telegram if enabled
            if schedule.post_to_telegram:
                self._post_to_telegram(blog_block)
            
            # Mark topic as completed
            topic.status = 'completed'
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error processing topic {topic.id}: {str(e)}")
            self._log_activity(topic, 'process_topic', 'failed', str(e))
            topic.status = 'failed'
            db.session.commit()
    
    def _translate_content(self, blog_block, target_languages):
        """Translate blog content to target languages"""
        for lang in target_languages:
            try:
                # Skip Ukrainian as it's the default language
                if lang.lower() == 'uk':
                    continue
                    
                result = self.openai_service.translate_content(blog_block.content, lang)
                if result.get('success'):
                    # Set the translated content based on language code
                    if lang.lower() == 'en':
                        blog_block.content_en = result.get('content')
                        blog_block.title_en = blog_block.title  # Also translate title in a real implementation
                        blog_block.summary_en = blog_block.summary
                    elif lang.lower() == 'de':
                        blog_block.content_de = result.get('content')
                        blog_block.title_de = blog_block.title
                        blog_block.summary_de = blog_block.summary
                    elif lang.lower() == 'ru':
                        blog_block.content_ru = result.get('content')
                        blog_block.title_ru = blog_block.title
                        blog_block.summary_ru = blog_block.summary
                        
                    db.session.commit()
                    self._log_activity(None, f'translate_to_{lang}', 'success', f"Content translated to {lang}")
                else:
                    self._log_activity(None, f'translate_to_{lang}', 'failed', result.get('error'))
            except Exception as e:
                logger.error(f"Error translating to {lang}: {str(e)}")
                self._log_activity(None, f'translate_to_{lang}', 'failed', str(e))
    
    def _generate_image(self, blog_block, topic):
        """Generate image for blog post"""
        try:
            # Generate DALL-E prompt
            prompt_result = self.openai_service.generate_image_prompt(
                topic.title, 
                topic.description
            )
            
            if not prompt_result.get('success'):
                self._log_activity(topic, 'generate_image_prompt', 'failed', prompt_result.get('error'))
                return
                
            image_prompt = prompt_result.get('prompt')
            self._log_activity(topic, 'generate_image_prompt', 'success', "Image prompt generated")
            
            # Generate image
            image_result = self.openai_service.generate_image(image_prompt)
            
            if not image_result.get('success'):
                self._log_activity(topic, 'generate_image', 'failed', image_result.get('error'))
                return
            
            # Download image
            image_url = image_result.get('url')
            response = requests.get(image_url)
            
            if response.status_code == 200:
                # Save image and update blog block
                filename = f"{secure_filename(topic.title)}-{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
                
                # Save the image using the application's file utility
                save_path = save_uploaded_file(
                    file_data=io.BytesIO(response.content),
                    folder='uploads/blog',
                    filename=filename
                )
                
                # Set the featured image on the blog block
                if save_path:
                    # Get just the filename part
                    if '/' in save_path:
                        blog_block.featured_image = save_path.split('/')[-1]
                    else:
                        blog_block.featured_image = save_path
                        
                    db.session.commit()
                    self._log_activity(topic, 'generate_image', 'success', "Image generated and saved")
            else:
                self._log_activity(topic, 'generate_image', 'failed', f"Failed to download image: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            self._log_activity(topic, 'generate_image', 'failed', str(e))
    
    def _post_to_telegram(self, blog_block):
        """Post blog content to Telegram"""
        try:
            image_path = None
            if blog_block.featured_image:
                image_path = os.path.join(
                    current_app.config['UPLOAD_FOLDER'],
                    'blog',
                    blog_block.featured_image
                )
                
            result = self.telegram_service.send_post(
                title=blog_block.title,
                text=blog_block.content[:1000] + "..." if len(blog_block.content) > 1000 else blog_block.content,
                image_url=image_path if os.path.exists(image_path) else None
            )
            
            if result.get('success'):
                self._log_activity(None, 'post_to_telegram', 'success', "Posted to Telegram")
            else:
                self._log_activity(None, 'post_to_telegram', 'failed', result.get('error'))
                
        except Exception as e:
            logger.error(f"Error posting to Telegram: {str(e)}")
            self._log_activity(None, 'post_to_telegram', 'failed', str(e))
    
    def _get_available_block_position(self):
        """Find an available block position"""
        # Check if we have any inactive blocks
        inactive_block = BlogBlock.query.filter_by(is_active=False).first()
        if inactive_block:
            return inactive_block.position
            
        # Otherwise return a position between 1-12 that has the oldest content
        oldest_block = BlogBlock.query.order_by(BlogBlock.updated_at).first()
        if oldest_block:
            return oldest_block.position
              # If no blocks exist, start with position 1
        return 1
    
    def _log_activity(self, topic, action, status, message):
        """Log automation activity"""
        try:
            # Use the new helper method
            ContentGenerationLog.add_log(
                topic=topic,
                action=action,
                status=status,
                message=message
            )
            
            logger.info(f"Blog automation: {action} - {status}: {message}")
        except Exception as e:
            # Failsafe logging in case of database errors
            logger.error(f"Error logging activity: {str(e)}")
            logger.info(f"Original message: {action} - {status}: {message}")
        
# Singleton instance
scheduler_instance = None

def get_scheduler(app=None):
    """Get or create the scheduler instance"""
    global scheduler_instance
    if scheduler_instance is None and app is not None:
        scheduler_instance = BlogAutomationScheduler(app)
    return scheduler_instance
