#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Fix Block Table Script for Render.com
This script specifically addresses the 'relation "block" does not exist' error
by directly creating the block table in PostgreSQL.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

def fix_block_table():
    """Creates the block table directly with SQL."""
    print("=== FIXING BLOCK TABLE ===")
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return False
    
    # Ensure proper PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        print("✓ Converted database URL from postgres:// to postgresql://")
      try:
        # Connect to the database
        print("Connecting to database...")
        engine = create_engine(db_url)
        
        # Check database encoding
        with engine.connect() as conn:
            result = conn.execute(text("SHOW SERVER_ENCODING"))
            server_encoding = result.scalar()
            print(f"Database server encoding: {server_encoding}")
            
            result = conn.execute(text("SHOW CLIENT_ENCODING"))
            client_encoding = result.scalar()
            print(f"Database client encoding: {client_encoding}")
            
            # Set client encoding to UTF8 explicitly
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            print("✅ Set client encoding to UTF8")
        
        # Check if block table exists
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Found tables: {', '.join(tables)}")
        
        if 'block' in tables:
            print("✅ Block table already exists!")
            
            # Test querying the block table
            try:
                with engine.connect() as conn:
                    result = conn.execute(text("SELECT COUNT(*) FROM block"))
                    count = result.scalar()
                    print(f"✅ Block table query successful: {count} records")
                return True
            except Exception as e:
                print(f"❌ Error querying block table: {e}")
                print("Will try to recreate it...")
          # Create the block table - create both Latin and Cyrillic versions
        print("Creating block table directly with SQL...")
        with engine.begin() as conn:
            # First drop existing tables if they exist
            conn.execute(text("""
            DROP TABLE IF EXISTS block CASCADE;
            """))
            conn.execute(text("""
            DROP TABLE IF EXISTS блок CASCADE;
            """))
            
            # Create block table with Latin name
            conn.execute(text("""
            CREATE TABLE block (
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
            
            # Also create a view with Cyrillic name
            print("Creating a view with Cyrillic name 'блок'...")
            conn.execute(text("""
            CREATE OR REPLACE VIEW блок AS SELECT * FROM block;
            """))
          # Verify the block table was created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        views = inspector.get_view_names()
        
        print(f"Tables after creation: {', '.join(tables)}")
        print(f"Views after creation: {', '.join(views)}")
        
        if 'block' in tables:
            print("✅ Block table (Latin) successfully created!")
            
            # Test querying the block table
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM block"))
                count = result.scalar()
                print(f"✅ Block table query successful: {count} records")
            
            # Try to query the Cyrillic view if it exists
            try:
                with engine.connect() as conn:
                    conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                    print("✅ Cyrillic 'блок' view is accessible")
            except Exception as e:
                print(f"⚠️ Could not access Cyrillic 'блок' view: {e}")
            
            return True
        else:
            print("⚠️ 'block' table not found in standard tables list")
            
            # Try direct query as a last resort
            try:
                with engine.connect() as conn:
                    conn.execute(text("SELECT COUNT(*) FROM block"))
                    print("✅ Block table exists but wasn't detected by inspector")
                    return True
            except Exception as e:
                print(f"❌ Failed to create or query block table: {e}")
                return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def fix_all_tables():
    """Fix all necessary tables."""
    print("\n=== FIXING ALL TABLES ===")
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return False
    
    # Ensure proper PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        engine = create_engine(db_url)
        
        # Create user table
        print("Creating user table...")
        with engine.begin() as conn:
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
        
        # Create other essential tables
        with engine.begin() as conn:
            # Settings table
            print("Creating settings table...")
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
            
            # Token table
            print("Creating token table...")
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
            
            # Category table
            print("Creating category table...")
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
            
            # Product table
            print("Creating product table...")
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
        
        # Create admin user
        print("Setting up admin user...")
        with engine.begin() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM \"user\" WHERE username = 'admin'"))
            if result.scalar() == 0:
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('admin')
                conn.execute(
                    text("INSERT INTO \"user\" (username, password_hash, is_admin) VALUES ('admin', :password_hash, TRUE)"),
                    {"password_hash": password_hash}
                )
                print("✅ Admin user created")
            else:
                print("✅ Admin user already exists")
        
        print("\n✅ All tables fixed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing tables: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("BLOCK TABLE FIX FOR RENDER.COM")
    print("This script addresses the 'relation \"block\" does not exist' error")
    print("=" * 60)
    
    block_fix_success = fix_block_table()
    
    if not block_fix_success:
        print("\n⚠️ Block table fix failed, trying to fix all tables...")
        all_tables_success = fix_all_tables()
        
        if all_tables_success:
            print("\n✅ DATABASE FIX COMPLETED SUCCESSFULLY!")
            sys.exit(0)
        else:
            print("\n❌ DATABASE FIX FAILED!")
            sys.exit(1)
    else:
        print("\n✅ BLOCK TABLE FIX COMPLETED SUCCESSFULLY!")
        sys.exit(0)
