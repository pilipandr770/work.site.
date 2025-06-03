#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Emergency Script to Create 'блок' (Cyrillic) Table
This script addresses the specific issue where the application expects a
Cyrillic table name 'блок' instead of Latin 'block'.
"""

import os
import sys
from sqlalchemy import create_engine, text

def create_cyrillic_block_table():
    """Create a block table with Cyrillic name 'блок'."""
    print("=== CREATING CYRILLIC 'БЛОК' TABLE ===")
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return False
    
    # Ensure proper PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Connect to database
        print("Connecting to database...")
        engine = create_engine(db_url)
        
        # Create block table with Cyrillic name
        print("Creating 'блок' table...")
        with engine.begin() as conn:
            # First drop existing table if it exists
            conn.execute(text('DROP TABLE IF EXISTS "блок" CASCADE'))
            
            # Create the table with Cyrillic name
            conn.execute(text('''
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
            '''))
        
        # Verify the table was created
        with engine.connect() as conn:
            try:
                result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                count = result.scalar()
                print(f"✅ 'блок' table created successfully: {count} records")
                return True
            except Exception as e:
                print(f"❌ Failed to query 'блок' table: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error creating 'блок' table: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("EMERGENCY CYRILLIC TABLE CREATION")
    print("=" * 60)
    
    success = create_cyrillic_block_table()
    
    if success:
        print("\n✅ Cyrillic 'блок' table created successfully!")
        sys.exit(0)
    else:
        print("\n❌ Failed to create Cyrillic 'блок' table!")
        sys.exit(1)
