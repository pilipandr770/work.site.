"""
Create blog automation tables directly if they don't exist
"""
from app import create_app, db
from sqlalchemy import inspect, text, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
import datetime

# Define models directly here to avoid circular imports
Base = declarative_base()

class BlogTopic(Base):
    """Topics for blog content generation"""
    __tablename__ = 'blog_topic'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    scheduled_for = Column(DateTime, nullable=True)
    blog_block_id = Column(Integer, ForeignKey('blog_block.id'), nullable=True)

class AutopostingSchedule(Base):
    """Schedule configuration for automated blog posting"""
    __tablename__ = 'autoposting_schedule'
    
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=False)
    days_of_week = Column(String(20), default='0,1,2,3,4,5,6')
    posting_time = Column(String(5), default='12:00')
    auto_translate = Column(Boolean, default=True)
    target_languages = Column(String(50), default='en,de,ru')
    generate_images = Column(Boolean, default=True)
    image_style = Column(String(100), default='professional, high quality')
    post_to_telegram = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ContentGenerationLog(Base):
    """Log of content generation activities"""
    __tablename__ = 'content_generation_log'
    
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('blog_topic.id'), nullable=True)
    action = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def create_tables():
    """Create all the required tables for blog automation"""
    app = create_app()
    with app.app_context():
        # Use direct SQL to make sure tables are created with proper columns and foreign keys
        print("Creating blog automation tables...")
        
        # Check which tables exist
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        
        # Create BlogTopic table if it doesn't exist
        if 'blog_topic' not in table_names:
            print("Creating BlogTopic table...")
            with db.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE blog_topic (
                        id SERIAL PRIMARY KEY,
                        title VARCHAR(255) NOT NULL,
                        description TEXT,
                        status VARCHAR(20) DEFAULT 'pending',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        scheduled_for TIMESTAMP,
                        blog_block_id INTEGER
                    )
                """))
                conn.commit()
                print("BlogTopic table created successfully")
        else:
            # Check if necessary columns exist
            print("BlogTopic table already exists, checking columns...")
            columns = [column['name'] for column in inspector.get_columns('blog_topic')]
            with db.engine.connect() as conn:
                if 'scheduled_for' not in columns:
                    print("Adding scheduled_for column to BlogTopic table...")
                    conn.execute(text("ALTER TABLE blog_topic ADD COLUMN scheduled_for TIMESTAMP"))
                    conn.commit()
                if 'blog_block_id' not in columns:
                    print("Adding blog_block_id column to BlogTopic table...")
                    conn.execute(text("ALTER TABLE blog_topic ADD COLUMN blog_block_id INTEGER"))
                    conn.commit()
        
        # Create AutopostingSchedule table if it doesn't exist
        if 'autoposting_schedule' not in table_names:
            print("Creating AutopostingSchedule table...")
            with db.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE autoposting_schedule (
                        id SERIAL PRIMARY KEY,
                        is_active BOOLEAN DEFAULT FALSE,
                        days_of_week VARCHAR(20) DEFAULT '0,1,2,3,4,5,6',
                        posting_time VARCHAR(5) DEFAULT '12:00',
                        auto_translate BOOLEAN DEFAULT TRUE,
                        target_languages VARCHAR(50) DEFAULT 'en,de,ru',
                        generate_images BOOLEAN DEFAULT TRUE,
                        image_style VARCHAR(100) DEFAULT 'professional, high quality',
                        post_to_telegram BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                print("AutopostingSchedule table created successfully")
        
        # Create ContentGenerationLog table if it doesn't exist
        if 'content_generation_log' not in table_names:
            print("Creating ContentGenerationLog table...")
            with db.engine.connect() as conn:
                conn.execute(text("""
                    CREATE TABLE content_generation_log (
                        id SERIAL PRIMARY KEY,
                        topic_id INTEGER,
                        action VARCHAR(50) NOT NULL,
                        status VARCHAR(20) NOT NULL,
                        message TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                conn.commit()
                print("ContentGenerationLog table created successfully")
        
        # Create a default AutopostingSchedule record
        try:
            with db.engine.connect() as conn:
                # Check if there are any records
                result = conn.execute(text("SELECT COUNT(*) FROM autoposting_schedule"))
                count = result.scalar()
                
                if count == 0:
                    print("Creating default AutopostingSchedule record")
                    conn.execute(
                        text("""
                        INSERT INTO autoposting_schedule 
                        (is_active, days_of_week, posting_time, auto_translate, target_languages, 
                         generate_images, image_style, post_to_telegram) 
                        VALUES 
                        (false, '0,1,2,3,4,5,6', '12:00', true, 'en,de,ru', true, 
                         'professional, high quality', false)
                        """)
                    )
                    conn.commit()
                    print("Default AutopostingSchedule record created")
        except Exception as e:
            print(f"Error creating default AutopostingSchedule record: {e}")
            
        print("Blog automation tables created successfully!")

if __name__ == "__main__":
    create_tables()
