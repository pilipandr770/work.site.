from app import create_app, db
from sqlalchemy import text

def add_duration_column():
    """Add the duration_seconds column to ContentGenerationLog table"""
    app = create_app()
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Check if column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='content_generation_log' AND column_name='duration_seconds'
                """))
                
                column_exists = result.fetchone()
                
                if not column_exists:
                    print("Adding duration_seconds column to ContentGenerationLog table...")
                    conn.execute(text("""
                        ALTER TABLE content_generation_log 
                        ADD COLUMN duration_seconds FLOAT
                    """))
                    conn.commit()
                    print("Column added successfully")
                else:
                    print("Column already exists")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    add_duration_column()
