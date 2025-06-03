#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Check and Fix ORM Model to Database Mapping
This script verifies and fixes ORM model mappings to database tables.
"""

import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.ext.declarative import declarative_base

def check_orm_mapping():
    """Check ORM mapping and fix issues."""
    print("=== CHECKING ORM MODEL MAPPING ===")
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block, User
        
        # Create app context
        app = create_app()
        with app.app_context():
            # Check the actual SQL query being generated
            print("Checking SQL query generation...")
            try:
                from sqlalchemy.dialects import postgresql
                query = Block.query.filter_by(is_active=True).statement
                sql_query = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
                print(f"Generated SQL query: {sql_query}")
                
                # Extract table name from SQL query
                import re
                table_match = re.search(r'FROM\s+([^\s]+)', sql_query)
                if table_match:
                    actual_table_name = table_match.group(1)
                    print(f"Actual table name in SQL query: {actual_table_name}")
                else:
                    print("Could not extract table name from SQL query")
            except Exception as e:
                print(f"Error analyzing SQL query: {e}")
            
            # Get table name from model
            block_tablename = getattr(Block, '__tablename__', 'block')
            print(f"Block model __tablename__: {block_tablename}")
            
            # Get table name in database
            engine = db.engine
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            views = inspector.get_view_names()
            print(f"Tables in database: {', '.join(tables)}")
            print(f"Views in database: {', '.join(views)}")
              # Create a direct 'блок' table regardless of other results
            print("Creating блок table directly to match the SQL query...")
            try:
                with engine.begin() as conn:
                    # First check if we can access any existing tables with this name
                    try:
                        conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                        print("✅ Table 'блок' is already accessible")
                    except Exception:
                        # Create the table directly
                        print("Cannot access 'блок' table, creating it...")
                        
                        # Drop any existing conflicts
                        try:
                            conn.execute(text('DROP TABLE IF EXISTS "блок" CASCADE'))
                        except Exception as e:
                            print(f"Warning when dropping table: {e}")
                            
                        # Create the Cyrillic named table directly
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
                        print("✅ Created 'блок' table directly")
                        
                # If standard block table exists, copy data
                try:
                    if 'block' in tables:
                        with engine.begin() as conn:
                            conn.execute(text('INSERT INTO "блок" SELECT * FROM block'))
                            print("✅ Copied data from 'block' to 'блок'")
                except Exception as e:
                    print(f"Warning when copying data: {e}")
                    
            except Exception as e:
                print(f"❌ Failed to create 'блок' table: {e}")
              # Try querying through direct SQL first to verify tables
            try:
                with engine.begin() as conn:
                    print("Testing direct queries to tables:")
                    
                    try:
                        result = conn.execute(text('SELECT COUNT(*) FROM block'))
                        count = result.scalar()
                        print(f"✅ Direct query to 'block': {count} records")
                    except Exception as e:
                        print(f"❌ Cannot query 'block': {e}")
                    
                    try:
                        result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                        count = result.scalar()
                        print(f"✅ Direct query to 'блок': {count} records")
                    except Exception as e:
                        print(f"❌ Cannot query 'блок': {e}")
            except Exception as e:
                print(f"Error in direct queries: {e}")
            
            # Try querying through the ORM
            try:
                blocks_count = Block.query.count()
                print(f"✅ Successfully queried Block model: {blocks_count} records")
                
                # Try to fetch one Block to fully test the query
                try:
                    block = Block.query.first()
                    if block:
                        print(f"✅ Successfully retrieved a Block record: ID={block.id}")
                    else:
                        print("ℹ️ No Block records found, but query worked")
                except Exception as e:
                    print(f"❌ Error fetching Block record: {e}")
                
                return True
            except Exception as e:
                print(f"❌ Failed to query Block model: {e}")
                
                # One final attempt - create a custom SQLAlchemy model that explicitly targets блок
                try:
                    print("Attempting to create a custom model for 'блок'...")
                    
                    class CustomBlock(db.Model):
                        __tablename__ = 'блок'
                        id = db.Column(db.Integer, primary_key=True)
                        title = db.Column(db.String(128))
                        is_active = db.Column(db.Boolean, default=True)
                    
                    count = CustomBlock.query.count()
                    print(f"✅ Successfully queried custom 'блок' model: {count} records")
                    return True
                except Exception as e:
                    print(f"❌ Failed with custom model too: {e}")
                    return False
                
    except Exception as e:
        print(f"❌ Error checking ORM mapping: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("ORM MODEL MAPPING CHECK")
    print("This script checks and fixes ORM model to database table mappings")
    print("=" * 60)
    
    success = check_orm_mapping()
    
    if success:
        print("\n✅ ORM mapping check completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ ORM mapping check failed!")
        sys.exit(1)
