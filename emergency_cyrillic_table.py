#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Emergency Cyrillic Table Creation Script
This script directly creates the 'блок' table using raw SQL commands.
It bypasses all other mechanisms and focuses solely on fixing the critical error.
"""

import os
import sys
from sqlalchemy import create_engine, text

def ensure_cyrillic_block_table():
    """Ensure the Cyrillic 'блок' table exists no matter what."""
    print("=== EMERGENCY CYRILLIC TABLE CREATION ===")
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found!")
        return False
    
    # Ensure correct PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        print("Connecting to database...")
        engine = create_engine(db_url)
        
        # Create the table using raw SQL
        print("Creating 'блок' table with direct SQL...")
        with engine.begin() as conn:
            # Set client encoding to UTF8
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            
            # Drop existing table if it exists
            conn.execute(text('DROP TABLE IF EXISTS "блок" CASCADE'))
            
            # Create the table
            conn.execute(text("""
            CREATE TABLE "блок" (
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
            
            # Add a sample record to ensure the table works
            conn.execute(text("""
            INSERT INTO "блок" (title, content, slug, is_active, is_top)
            VALUES ('Welcome', 'Welcome to IT Token', 'welcome', TRUE, TRUE)
            """))
        
        # Verify the table was created
        with engine.connect() as conn:
            # Set client encoding to UTF8
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            
            # Test querying the table
            result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
            count = result.scalar()
            
            if count > 0:
                print(f"✅ Success! 'блок' table created with {count} records")
                return True
            else:
                print("⚠️ Table created but no records found")
                return False
    
    except Exception as e:
        print(f"❌ Error creating Cyrillic table: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("EMERGENCY CYRILLIC TABLE CREATION")
    print("This script directly creates the 'блок' table using raw SQL commands")
    print("=" * 60)
    
    success = ensure_cyrillic_block_table()
    
    if success:
        print("\n✅ CYRILLIC TABLE CREATION COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ CYRILLIC TABLE CREATION FAILED!")
        sys.exit(1)
