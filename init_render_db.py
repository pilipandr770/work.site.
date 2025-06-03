#!/usr/bin/env python
# init_render_db.py

"""
Script to initialize the database tables on Render.com
Run this script manually in the shell if the prestart.sh script fails.
"""

import os
import sys
from pathlib import Path
from sqlalchemy import inspect, create_engine, text

def setup_environment():
    """Set up the environment for database initialization."""
    print("Setting up environment...")
    
    # Add the current directory to Python path
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        env_path = current_dir / '.env'
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Environment variables loaded from {env_path}")
    except ImportError:
        print("Warning: python-dotenv not installed")
    
    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        db_type = "PostgreSQL" if "postgres" in db_url else "SQLite"
        print(f"Found database connection string ({db_type})")
    else:
        print("Warning: DATABASE_URL not found in environment variables")

def run_migrations():
    """Run database migrations to create or update tables."""
    print("\nRunning database migrations...")
    
    try:
        from app import create_app, db
        from app.models import User, Block
        
        # Create app context and tables
        app = create_app()
        with app.app_context():
            print("Creating all database tables...")
            db.create_all()
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                from werkzeug.security import generate_password_hash
                admin = User(
                    username='admin',
                    password_hash=generate_password_hash('admin'),
                    is_admin=True
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created: username='admin', password='admin'")
            else:
                print("✅ Admin user already exists")
                
        print("✅ Migrations completed successfully!")
        return True
    except Exception as e:
        print(f"❌ Error during migrations: {e}")
        return False

def verify_tables():
    """Verify that database tables exist."""
    print("\nVerifying created tables...")
    
    try:
        # Import the database connection
        from app import create_app, db
        from app.models import User, Block
        
        # Create a temporary application context
        with create_app().app_context():
            # Run a query to get table names
            engine = db.engine
            inspector = db.inspect(engine)
            tables = inspector.get_table_names()
            
            if tables:
                print(f"✅ Found {len(tables)} tables in the database:")
                required_tables = ['block', 'user', 'settings', 'token', 'category', 'product']
                for table in sorted(tables):
                    status = "✓" if table in required_tables else "-"
                    print(f"  {status} {table}")
                    
                # Specifically check for the Block table
                if 'block' in tables:
                    block_count = Block.query.count()
                    print(f"\n✅ Block table exists and has {block_count} records")
                else:
                    print("\n❌ Block table does not exist! This is causing the error.")
                
                return True
            else:
                print("❌ No tables found in the database!")
                return False
    except Exception as e:
        print(f"❌ Error checking tables: {e}")
        return False

def main():
    """Run the database initialization process."""
    print("=" * 50)
    print("DATABASE INITIALIZATION ON RENDER.COM")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Run migrations
    migrations_success = run_migrations()
    
    # Verify tables
    if migrations_success:
        tables_success = verify_tables()
    else:
        tables_success = False
      print("\n" + "=" * 50)
    if migrations_success and tables_success:
        print("✅ DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
        print("Your application should now work correctly.")
    else:
        print("❌ DATABASE INITIALIZATION COMPLETED WITH ERRORS")
        print("Please check the logs above to identify the issues.")
    print("=" * 50)

if __name__ == "__main__":
    main()
