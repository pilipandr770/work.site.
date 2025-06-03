#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct database initialization script for Render.com
This is a simplified script that directly creates database tables.
Use this if other methods fail.
"""

import sys
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, create_engine

def main():
    try:
        print("=== DIRECT DATABASE INITIALIZATION ===")
        
        # Import app components
        try:
            print("Importing application modules...")
            from app import create_app, db
            from app.models import User, Block, Settings, Token, Category, Product
            from werkzeug.security import generate_password_hash
        except ImportError as e:
            print(f"Error importing modules: {e}")
            return False
        
        # Create app with context
        try:
            print("Creating application context...")
            app = create_app()
        except Exception as e:
            print(f"Error creating app: {e}")
            return False
          # Create tables and admin user
        with app.app_context():
            try:
                print("Creating all tables with ORM...")
                db.create_all()
                print("✅ Tables created successfully with ORM!")
                
                # Ensure tables are correctly created by executing a direct SQL query
                print("Verifying table creation with direct SQL...")
                engine = db.engine
                inspector = db.inspect(engine)
                tables = inspector.get_table_names()
                
                print(f"Tables in database: {', '.join(tables)}")
                
                # If 'block' table is missing, create it directly with SQL
                if 'block' not in tables:
                    print("⚠️ Block table not found - creating it directly with SQL...")
                    with engine.connect() as conn:
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
                        conn.commit()
                        print("✅ Block table created directly with SQL!")
                
                # Check for admin user and create if needed
                print("Checking for admin user...")
                admin = User.query.filter_by(username='admin').first()
                if not admin:
                    print("Creating admin user...")
                    admin = User(
                        username='admin',
                        password_hash=generate_password_hash('admin'),
                        is_admin=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Admin user created successfully!")
                else:
                    print("✅ Admin user already exists")
                
                # Verify key tables exist again
                try:
                    print("Verifying Block table...")
                    block_count = Block.query.count()
                    print(f"✅ Block table exists with {block_count} records")
                except Exception as e:
                    print(f"❌ Error verifying Block table: {e}")
                    print("Trying direct SQL query...")
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT COUNT(*) FROM block"))
                        count = result.scalar()
                        print(f"✅ Block table exists with {count} records (SQL)")
                
                return True
                
            except SQLAlchemyError as e:
                print(f"SQLAlchemy error: {e}")
                return False
                
            except Exception as e:
                print(f"Unexpected error: {e}")
                return False
    
    except Exception as e:
        print(f"Global error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Direct database initialization completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Direct database initialization failed!")
        sys.exit(1)
