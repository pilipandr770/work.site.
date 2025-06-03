#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Definitive Cyrillic Block Table Fix
This script provides a comprehensive solution to the issue with the Block model and its table in PostgreSQL.
It properly handles the Cyrillic vs Latin table name issue by:
1. Checking existing tables in the database
2. Explicitly setting the correct table name for the Block model
3. Creating the table if it doesn't exist
4. Transferring data between tables if needed
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def get_database_url():
    """Get the database URL from environment variables."""
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return None
    
    # Fix for PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    return db_url

def check_tables_in_database(engine):
    """Check which tables exist in the database."""
    print("Checking existing tables in the database...")
    
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print(f"Found tables: {tables}")
    
    latin_block_exists = 'block' in tables
    cyrillic_block_exists = 'блок' in tables
    
    return {
        'latin_block': latin_block_exists,
        'cyrillic_block': cyrillic_block_exists,
        'all_tables': tables
    }

def check_block_model():
    """Check the Block model configuration."""
    try:
        from app import create_app, db
        from app.models import Block
        
        # Get the current tablename
        tablename = getattr(Block, '__tablename__', None)
        print(f"Current Block.__tablename__ = {tablename}")
        
        return tablename
    except Exception as e:
        print(f"❌ Error checking Block model: {e}")
        return None

def create_cyrillic_table(engine):
    """Create the Cyrillic 'блок' table."""
    print("Creating 'блок' table with direct SQL...")
    
    try:
        with engine.begin() as conn:
            # Set client encoding to UTF8
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            
            # Create the table
            conn.execute(text("""
            CREATE TABLE IF NOT EXISTS "блок" (
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
                content_de TEXT,
                content_ru TEXT
            )
            """))
        return True
    except Exception as e:
        print(f"❌ Error creating Cyrillic table: {e}")
        return False

def transfer_data_between_tables(engine, source_table, target_table):
    """Transfer data from one table to another."""
    print(f"Transferring data from '{source_table}' to '{target_table}'...")
    
    try:
        with engine.begin() as conn:
            # Set client encoding to UTF8
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            
            # Check if source table has any data
            result = conn.execute(text(f'SELECT COUNT(*) FROM "{source_table}"'))
            count = result.scalar()
            
            if count == 0:
                print(f"ℹ️ Source table '{source_table}' is empty, no data to transfer")
                return True
            
            # Transfer data
            conn.execute(text(f"""
            INSERT INTO "{target_table}" (
                id, title, content, image, "order", is_active, slug, is_top,
                title_ua, title_en, title_de, title_ru,
                content_ua, content_en, content_de, content_ru
            )
            SELECT 
                id, title, content, image, "order", is_active, slug, is_top,
                title_ua, title_en, title_de, title_ru,
                content_ua, content_en, content_de, content_ru
            FROM "{source_table}"
            ON CONFLICT (id) DO NOTHING
            """))
            
            print(f"✅ Data transferred from '{source_table}' to '{target_table}'")
            return True
    except Exception as e:
        print(f"❌ Error transferring data: {e}")
        return False

def update_block_model_tablename():
    """Update the Block model to use the Cyrillic table name."""
    try:
        from app import create_app, db
        from app.models import Block
        
        # Set the tablename explicitly
        Block.__tablename__ = 'блок'
        print(f"Updated Block.__tablename__ = {Block.__tablename__}")
        
        # Create app context and test the model
        app = create_app()
        with app.app_context():
            # Test the model works
            count = Block.query.count()
            print(f"Block.query.count() = {count}")
            
        return True
    except Exception as e:
        print(f"❌ Error updating Block model tablename: {e}")
        return False

def modify_models_file():
    """Modify the models.py file to explicitly set the Cyrillic table name."""
    try:
        import os
        import shutil
        from pathlib import Path
        
        models_file = Path("app/models.py")
        backup_file = Path("app/models.py.bak")
        
        if not models_file.exists():
            print(f"❌ Models file {models_file} not found!")
            return False
        
        # Make a backup if it doesn't exist
        if not backup_file.exists():
            print(f"Creating backup of {models_file} to {backup_file}")
            shutil.copy2(models_file, backup_file)
        
        # Read the file
        with open(models_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Find the Block class definition
        block_class_idx = content.find("class Block(db.Model):")
        if block_class_idx == -1:
            print("❌ Could not find Block class definition in models.py!")
            return False
        
        # Check if __tablename__ is already defined
        if '__tablename__' in content[block_class_idx:block_class_idx+200]:
            print("ℹ️ __tablename__ is already defined in Block class")
            
            # Replace existing __tablename__ with Cyrillic one
            import re
            pattern = r'(class Block\(db\.Model\):.*?)(__tablename__\s*=\s*[\'"].*?[\'"])'
            replacement = r'\1__tablename__ = "блок"  # Explicit Cyrillic table name'
            new_content = re.sub(pattern, replacement, content[block_class_idx:], count=1, flags=re.DOTALL)
            
            if new_content != content[block_class_idx:]:
                final_content = content[:block_class_idx] + new_content
                with open(models_file, 'w', encoding='utf-8') as file:
                    file.write(final_content)
                print("✅ Replaced existing __tablename__ with Cyrillic one")
            else:
                print("ℹ️ No changes needed to __tablename__")
                
            return True
        
        # Insert __tablename__ attribute after class definition
        class_def_end = content.find(":", block_class_idx) + 1
        modified_content = (
            content[:class_def_end] + 
            '\n    __tablename__ = "блок"  # Explicit Cyrillic table name' +
            content[class_def_end:]
        )
        
        # Write modified content back to file
        with open(models_file, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        
        print("✅ Added explicit Cyrillic __tablename__ to Block class")
        return True
    except Exception as e:
        print(f"❌ Error modifying models file: {e}")
        return False

def fix_block_table_definitive():
    """Main function to fix the block table issue definitively."""
    print("=" * 60)
    print("DEFINITIVE CYRILLIC BLOCK TABLE FIX")
    print("=" * 60)
    
    # Get database URL
    db_url = get_database_url()
    if not db_url:
        return False
    
    # Connect to database with SQLAlchemy
    try:
        engine = create_engine(db_url)
        
        # Check existing tables
        tables_info = check_tables_in_database(engine)
        latin_block_exists = tables_info['latin_block']
        cyrillic_block_exists = tables_info['cyrillic_block']
        
        # Check block model configuration
        current_tablename = check_block_model()
        
        print("\n--- DIAGNOSIS ---")
        print(f"Latin 'block' table exists: {latin_block_exists}")
        print(f"Cyrillic 'блок' table exists: {cyrillic_block_exists}")
        print(f"Block model tablename: {current_tablename}")
        print("----------------\n")
        
        # Action plan based on diagnosis
        print("--- ACTION PLAN ---")
        
        # Step 1: Modify models file to use Cyrillic table name
        print("\n[1] Modifying models file...")
        modify_models_file()
        
        # Step 2: Create Cyrillic table if needed
        if not cyrillic_block_exists:
            print("\n[2] Creating Cyrillic 'блок' table...")
            create_cyrillic_table(engine)
        else:
            print("\n[2] Cyrillic 'блок' table already exists")
        
        # Step 3: Transfer data from Latin to Cyrillic table if needed
        if latin_block_exists and cyrillic_block_exists:
            print("\n[3] Transferring data from Latin to Cyrillic table...")
            transfer_data_between_tables(engine, 'block', 'блок')
        else:
            print("\n[3] No data transfer needed")
        
        # Step 4: Update Block model to use Cyrillic table name
        print("\n[4] Updating Block model to use Cyrillic table name...")
        update_block_model_tablename()
        
        print("\n--- VERIFICATION ---")
        # Re-check tables after fixes
        tables_info = check_tables_in_database(engine)
        cyrillic_block_exists = tables_info['cyrillic_block']
        
        if cyrillic_block_exists:
            # Verify we can query the table
            try:
                with engine.connect() as conn:
                    conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
                    result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                    count = result.scalar()
                    print(f"✅ Successfully queried 'блок' table: {count} records found")
                return True
            except Exception as e:
                print(f"❌ Error verifying Cyrillic table: {e}")
                return False
        else:
            print("❌ Cyrillic 'блок' table still doesn't exist after fixes!")
            return False
        
    except Exception as e:
        print(f"❌ Error connecting to database: {e}")
        return False

if __name__ == "__main__":
    success = fix_block_table_definitive()
    
    if success:
        print("\n✅ BLOCK TABLE ISSUE FIXED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ FAILED TO FIX BLOCK TABLE ISSUE!")
        sys.exit(1)
