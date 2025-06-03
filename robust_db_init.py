#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Robust Database Initialization Script for Render.com

This script provides multiple strategies to initialize the database:
1. Standard ORM approach using db.create_all()
2. Direct SQL approach if ORM fails
3. Verification and retry mechanism

Usage:
    python robust_db_init.py [--force-sql]
"""

import os
import sys
import time
import argparse
from pathlib import Path
from sqlalchemy import inspect, create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Number of retries for database operations
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def setup_environment():
    """Set up the environment for database initialization."""
    print("\n=== Setting up environment ===")
    
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
            print(f"✅ Environment variables loaded from {env_path}")
    except ImportError:
        print("ℹ️ python-dotenv not installed, using system environment")
    
    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if db_url:
        db_type = "PostgreSQL" if "postgres" in db_url else "SQLite"
        # Mask the password for security
        masked_url = db_url
        if '@' in masked_url:
            parts = masked_url.split('@')
            auth = parts[0].split('://')
            masked_url = f"{auth[0]}://****:****@{parts[1]}"
        print(f"✅ Found database connection: {db_type} ({masked_url})")
        
        # Convert postgres:// to postgresql:// if needed
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
            os.environ['DATABASE_URL'] = db_url
            print("✅ Converted postgres:// to postgresql:// in connection string")
    else:
        print("❌ DATABASE_URL not found in environment variables")
        print("   Using fallback to SQLite (this won't work on Render)")
    
    return True

def check_connection():
    """Verify database connection."""
    print("\n=== Checking database connection ===")
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not found")
        return False
    
    # Convert postgres:// to postgresql:// if needed
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("Attempting to connect to database...")
        engine = create_engine(db_url)
        connection = engine.connect()
        connection.close()
        print("✅ Successfully connected to database!")
        return True
    except SQLAlchemyError as e:
        print(f"❌ Database connection error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def initialize_with_orm():
    """Initialize database using SQLAlchemy ORM."""
    print("\n=== Initializing database with SQLAlchemy ORM ===")
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"Attempt {attempt}/{MAX_RETRIES}...")
            
            # Import from app
            from app import create_app, db
            from app.models import User, Block, Settings, Token, Category, Product
            
            # Create app context
            app = create_app()
            with app.app_context():
                print("Creating all database tables...")
                db.create_all()
                print("✅ Tables created successfully with ORM")
                
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
                
                # Verify the Block table exists and is accessible
                try:
                    block_count = Block.query.count()
                    print(f"✅ Block table successfully created with {block_count} records")
                except Exception as e:
                    print(f"❌ Error accessing Block table: {e}")
                    raise
                
            return True
            
        except Exception as e:
            print(f"❌ Error in ORM initialization (attempt {attempt}): {e}")
            if attempt < MAX_RETRIES:
                print(f"Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                print("❌ ORM initialization failed after all attempts")
                return False

def initialize_with_sql():
    """Initialize database using direct SQL commands."""
    print("\n=== Initializing database with direct SQL ===")
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not found")
        return False
    
    # Convert postgres:// to postgresql:// if needed
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        engine = create_engine(db_url)
        
        # Create tables with SQL
        with engine.begin() as conn:
            print("Creating User table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS "user" (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(64) UNIQUE,
                    password_hash VARCHAR(128),
                    wallet_address VARCHAR(42),
                    is_admin BOOLEAN DEFAULT FALSE,
                    token_balance FLOAT DEFAULT 0.0
                )
            """))
            
            print("Creating Block table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS block (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(128),
                    content TEXT,
                    image VARCHAR(256),
                    "order" INTEGER DEFAULT 1,
                    is_active BOOLEAN DEFAULT TRUE,
                    slug VARCHAR(64) UNIQUE,
                    is_top BOOLEAN DEFAULT FALSE,
                    title_ua VARCHAR(128),
                    title_en VARCHAR(128),
                    title_de VARCHAR(128),
                    title_ru VARCHAR(128),
                    content_ua TEXT,
                    content_en TEXT,
                    content_ru TEXT,
                    content_de TEXT
                )
            """))
            
            print("Creating Settings table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS settings (
                    id SERIAL PRIMARY KEY,
                    site_name VARCHAR(128),
                    email VARCHAR(128),
                    phone VARCHAR(32),
                    address VARCHAR(256),
                    about_text TEXT,
                    meta_keywords TEXT,
                    meta_description TEXT,
                    telegram_link VARCHAR(256),
                    facebook_link VARCHAR(256),
                    instagram_link VARCHAR(256),
                    twitter_link VARCHAR(256),
                    site_name_ua VARCHAR(128),
                    site_name_en VARCHAR(128),
                    site_name_ru VARCHAR(128),
                    about_text_ua TEXT,
                    about_text_en TEXT,
                    about_text_ru TEXT
                )
            """))
            
            print("Creating Token table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS token (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64),
                    symbol VARCHAR(8),
                    decimals INTEGER DEFAULT 18,
                    total_supply FLOAT,
                    contract_address VARCHAR(42),
                    network_name VARCHAR(32),
                    owner_address VARCHAR(42),
                    block_explorer_url VARCHAR(256)
                )
            """))
            
            print("Creating Category table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS category (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(64),
                    description TEXT,
                    image VARCHAR(256),
                    is_active BOOLEAN DEFAULT TRUE,
                    name_ua VARCHAR(64),
                    name_en VARCHAR(64),
                    name_ru VARCHAR(64),
                    description_ua TEXT,
                    description_en TEXT,
                    description_ru TEXT
                )
            """))
            
            print("Creating Product table...")
            conn.execute(text("""
                CREATE TABLE IF NOT EXISTS product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(128),
                    description TEXT,
                    price FLOAT,
                    image VARCHAR(256),
                    is_active BOOLEAN DEFAULT TRUE,
                    category_id INTEGER REFERENCES category(id),
                    token_price FLOAT,
                    name_ua VARCHAR(128),
                    name_en VARCHAR(128),
                    name_ru VARCHAR(128),
                    description_ua TEXT,
                    description_en TEXT,
                    description_ru TEXT
                )
            """))
            
            # Check if admin user exists, create if not
            admin_exists = conn.execute(text("SELECT COUNT(*) FROM \"user\" WHERE username = 'admin'")).scalar()
            if not admin_exists:
                print("Creating admin user...")
                # Need to import for password hashing
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('admin')
                conn.execute(text(
                    "INSERT INTO \"user\" (username, password_hash, is_admin) VALUES ('admin', :password_hash, TRUE)"
                ), {"password_hash": password_hash})
                print("✅ Admin user created: username='admin', password='admin'")
            else:
                print("✅ Admin user already exists")
        
        print("✅ Tables created successfully with direct SQL")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ SQL Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def verify_tables():
    """Verify database tables exist and are accessible."""
    print("\n=== Verifying database tables ===")
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not found")
        return False
    
    # Convert postgres:// to postgresql:// if needed
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Check tables with SQLAlchemy inspector
        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("❌ No tables found in database!")
            return False
        
        print(f"✅ Found {len(tables)} tables in database:")
        
        # Key tables we need for the app
        required_tables = ['block', 'user', 'settings', 'token', 'category', 'product']
        missing_tables = [table for table in required_tables if table not in tables]
        
        for table in sorted(tables):
            status = "✓" if table in required_tables else "-"
            print(f"  {status} {table}")
        
        if missing_tables:
            print(f"❌ Missing required tables: {', '.join(missing_tables)}")
            return False
        
        # Test query on block table
        with engine.connect() as conn:
            try:
                block_count = conn.execute(text("SELECT COUNT(*) FROM block")).scalar()
                print(f"✅ Block table query successful: {block_count} records")
            except Exception as e:
                print(f"❌ Error querying block table: {e}")
                return False
            
            try:
                admin_count = conn.execute(text("SELECT COUNT(*) FROM \"user\" WHERE is_admin = true")).scalar()
                print(f"✅ Admin user query successful: {admin_count} administrators")
            except Exception as e:
                print(f"❌ Error querying user table: {e}")
                return False
        
        print("✅ All required tables verified!")
        return True
    
    except SQLAlchemyError as e:
        print(f"❌ Database error during verification: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during verification: {e}")
        return False

def main():
    """Run the robust database initialization process."""
    parser = argparse.ArgumentParser(description='Robust database initialization')
    parser.add_argument('--force-sql', action='store_true', help='Skip ORM and use SQL directly')
    args = parser.parse_args()
    
    print("=" * 60)
    print("ROBUST DATABASE INITIALIZATION FOR RENDER.COM")
    print("=" * 60)
    
    # Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        sys.exit(1)
    
    # Check database connection
    if not check_connection():
        print("❌ Database connection failed")
        sys.exit(1)
    
    # Initialize database
    success = False
    
    if not args.force_sql:
        # Try ORM first
        success = initialize_with_orm()
    
    if not success:
        # Fall back to SQL if ORM failed or --force-sql was specified
        print("Falling back to direct SQL initialization...")
        success = initialize_with_sql()
    
    # Verify tables
    verify_success = verify_tables()
    
    # Final status
    print("\n" + "=" * 60)
    if success and verify_success:
        print("✅ DATABASE INITIALIZATION COMPLETED SUCCESSFULLY!")
        print("Your application should now work correctly.")
    else:
        print("❌ DATABASE INITIALIZATION COMPLETED WITH ISSUES")
        print("Please check the logs above to identify and fix problems.")
    print("=" * 60 + "\n")
    
    if not verify_success:
        sys.exit(1)

if __name__ == "__main__":
    main()
