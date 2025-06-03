#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct Fix for Block Model Table Name
This script directly modifies the Block model to point to the correct table name.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect

def fix_block_model():
    """Fix the Block model directly to point to the correct table name."""
    print("=== DIRECT BLOCK MODEL FIX ===")
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block
        
        # Get the original tablename
        original_tablename = getattr(Block, '__tablename__', 'block')
        print(f"Original Block.__tablename__ = {original_tablename}")
        
        # Force the correct Cyrillic table name
        Block.__tablename__ = 'блок'
        print(f"Modified Block.__tablename__ = {Block.__tablename__}")
        
        # Create the app context
        app = create_app()
        with app.app_context():
            # Create the table with the Cyrillic name
            print("Creating 'блок' table...")
            engine = db.engine
            with engine.begin() as conn:
                conn.execute(text("""
                DROP TABLE IF EXISTS "блок" CASCADE;
                
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
            
            # Test querying with the modified model
            try:
                count = Block.query.count()
                print(f"✅ Successfully queried Block with Cyrillic name: {count} records")
                
                # Create a test record
                try:
                    test_block = Block(
                        title="Test Block",
                        content="This is a test block to verify the table works",
                        slug="test-block",
                        is_active=True
                    )
                    db.session.add(test_block)
                    db.session.commit()
                    print(f"✅ Successfully created a test block with ID: {test_block.id}")
                except Exception as e:
                    print(f"❌ Failed to create test block: {e}")
                
                return True
            except Exception as e:
                print(f"❌ Failed to query Block with Cyrillic name: {e}")
                return False
    
    except Exception as e:
        print(f"❌ Error fixing Block model: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DIRECT BLOCK MODEL FIX")
    print("This script directly modifies the Block model to point to the Cyrillic table name")
    print("=" * 60)
    
    success = fix_block_model()
    
    if success:
        print("\n✅ Block model fix completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Block model fix failed!")
        sys.exit(1)
