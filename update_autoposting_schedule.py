from app import create_app, db
from app.blog_automation.models import AutopostingSchedule
from datetime import datetime

def update_autoposting_schedule():
    """Update autoposting schedule to test functionality"""
    app = create_app()
    with app.app_context():
        # Get or create settings
        settings = AutopostingSchedule.query.first()
        if not settings:
            settings = AutopostingSchedule()
            db.session.add(settings)
        
        # Set current time for immediate testing
        now = datetime.utcnow()
        current_time = f"{now.hour}:{now.minute}"
        current_day = str(now.weekday())  # 0-6, Monday is 0
        
        # Update settings for immediate run
        settings.is_active = True
        settings.days_of_week = current_day
        settings.posting_time = current_time
        settings.auto_translate = True
        settings.target_languages = 'en'  # Just English for faster testing
        settings.generate_images = True
        settings.post_to_telegram = False  # Set to True if you want to test Telegram posting
        
        db.session.commit()
        print(f"Autoposting schedule updated for immediate run (day: {current_day}, time: {current_time})")

if __name__ == "__main__":
    update_autoposting_schedule()
