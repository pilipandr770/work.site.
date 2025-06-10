from app import create_app, db
from app.blog_automation.models import BlogTopic

def add_test_topic():
    """Add a test topic to the database"""
    app = create_app()
    with app.app_context():
        # Check if table exists
        try:
            test_topic = BlogTopic(
                title='Інновації у сфері цифрових технологій',
                description='Blockchain AI IoT цифрова трансформація',
                status='pending'
            )
            
            db.session.add(test_topic)
            db.session.commit()
            print('Test topic added successfully')
            return True
        except Exception as e:
            print(f"Error adding test topic: {str(e)}")
            return False

if __name__ == "__main__":
    add_test_topic()
