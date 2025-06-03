#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct SQL script for creating database tables on Render.com.
This script is a last resort if all other methods fail.
It directly executes SQL commands to create tables without using SQLAlchemy ORM.
"""

import os
import sys
from sqlalchemy import create_engine, text

def create_tables():
    """Create database tables using direct SQL."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set!")
        return False
    
    # Convert postgres:// to postgresql:// if needed
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("Connecting to database...")
        engine = create_engine(db_url)
        
        with engine.begin() as conn:
            print("\nCreating database tables...")
            
            # Create user table
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
            
            # Create block table
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
            
            # Create settings table
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
            
            # Create token table
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
            
            # Create category table
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
            
            # Create product table
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
            
            # Create order table
            print("Creating Order table...")
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS "order" (
                id SERIAL PRIMARY KEY,
                user_id INTEGER,
                status VARCHAR(32),
                total_price FLOAT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                payment_method VARCHAR(32),
                shipping_address TEXT,
                contact_phone VARCHAR(32),
                contact_email VARCHAR(128),
                shipping_country VARCHAR(64),
                shipping_city VARCHAR(64),
                shipping_zip VARCHAR(32),
                payment_id VARCHAR(128)
            )
            """))
            
            # Create order_item table
            print("Creating OrderItem table...")
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS order_item (
                id SERIAL PRIMARY KEY,
                order_id INTEGER REFERENCES "order"(id),
                product_id INTEGER REFERENCES product(id),
                quantity INTEGER,
                price FLOAT
            )
            """))

        # Create admin user
        with engine.begin() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM \"user\" WHERE username = 'admin'"))
            if result.scalar() == 0:
                from werkzeug.security import generate_password_hash
                password_hash = generate_password_hash('admin')
                
                print("Creating admin user...")
                conn.execute(text(
                    "INSERT INTO \"user\" (username, password_hash, is_admin) VALUES ('admin', :password_hash, TRUE)"
                ), {"password_hash": password_hash})
                print("✅ Admin user created successfully!")
            else:
                print("✅ Admin user already exists")
                
        print("\n✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        return False

def verify_tables():
    """Verify that tables were created."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        return False
    
    # Convert postgres:// to postgresql:// if needed
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("\nVerifying tables...")
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            
            required_tables = ['user', 'block', 'settings', 'token', 'category', 'product']
            missing_tables = [table for table in required_tables if table not in tables]
            
            print(f"\nTables in database ({len(tables)}):")
            for table in sorted(tables):
                status = "✓" if table in required_tables else "-"
                print(f"  {status} {table}")
            
            if missing_tables:
                print(f"\n❌ Missing tables: {', '.join(missing_tables)}")
                return False
                
            print("\n✅ All required tables exist!")
            return True
            
    except Exception as e:
        print(f"\n❌ Error verifying tables: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DIRECT SQL DATABASE INITIALIZATION")
    print("This script creates tables directly with SQL commands")
    print("=" * 60)
    
    if create_tables():
        verify_tables()
        print("\n✅ Direct SQL initialization completed!")
    else:
        print("\n❌ Direct SQL initialization failed!")
        sys.exit(1)
