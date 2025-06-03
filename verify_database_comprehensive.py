#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Comprehensive Database Table Verification Script
This script performs detailed checks on the database tables, specifically focusing on the 'блок' table,
and reports detailed diagnostics to help identify and troubleshoot any remaining issues.
"""

import os
import sys
import json
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError
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

def check_database_connection(db_url):
    """Check if we can connect to the database."""
    print("Checking database connection...")
    
    try:
        # Connect with SQLAlchemy
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful with SQLAlchemy")
        
        # Connect with psycopg2 for more direct control
        db_params = {}
        if '://' in db_url:
            # Parse connection string
            from urllib.parse import urlparse
            parsed = urlparse(db_url)
            db_params = {
                'dbname': parsed.path[1:],
                'user': parsed.username,
                'password': parsed.password,
                'host': parsed.hostname,
                'port': parsed.port
            }
        
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Direct psycopg2 connection successful: {version[0]}")
        conn.close()
        
        return engine
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def check_tables_in_database(engine):
    """Check which tables exist in the database and their properties."""
    print("\nExamining database tables...")
    
    try:
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        print(f"All tables in database: {', '.join(tables)}")
        
        # Check for both Latin and Cyrillic tables
        latin_block_exists = 'block' in tables
        cyrillic_block_exists = 'блок' in tables
        
        print(f"Latin 'block' table exists: {latin_block_exists}")
        print(f"Cyrillic 'блок' table exists: {cyrillic_block_exists}")
        
        # Get table details for debugging
        table_details = {}
        for table_name in tables:
            columns = []
            for column in inspector.get_columns(table_name):
                columns.append({
                    'name': column['name'],
                    'type': str(column['type']),
                    'nullable': column['nullable']
                })
            
            pk = []
            for primary_key in inspector.get_pk_constraint(table_name).get('constrained_columns', []):
                pk.append(primary_key)
            
            table_details[table_name] = {
                'columns': columns,
                'primary_key': pk
            }
        
        return {
            'latin_block': latin_block_exists,
            'cyrillic_block': cyrillic_block_exists,
            'all_tables': tables,
            'table_details': table_details
        }
    except Exception as e:
        print(f"❌ Error inspecting database tables: {e}")
        return {
            'latin_block': False,
            'cyrillic_block': False,
            'all_tables': [],
            'table_details': {},
            'error': str(e)
        }

def check_queries(engine):
    """Check if we can query the tables directly."""
    print("\nTesting direct queries...")
    
    try:
        # Test query to Cyrillic table
        with engine.connect() as conn:
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            try:
                result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                count = result.scalar()
                print(f"✅ Successfully queried 'блок' table: {count} records")
            except Exception as e:
                print(f"❌ Failed to query 'блок' table: {e}")
        
        # Test query to Latin table
        with engine.connect() as conn:
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            try:
                result = conn.execute(text('SELECT COUNT(*) FROM "block"'))
                count = result.scalar()
                print(f"✅ Successfully queried 'block' table: {count} records")
            except Exception as e:
                print(f"❌ Failed to query 'block' table: {e}")
                
        return True
    except Exception as e:
        print(f"❌ Error executing queries: {e}")
        return False

def check_orm_query():
    """Check if we can query using the ORM."""
    print("\nTesting ORM queries...")
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block
        
        # Get the current tablename
        tablename = getattr(Block, '__tablename__', None)
        print(f"Block.__tablename__ = {tablename}")
        
        # Create app context and test the model
        app = create_app()
        with app.app_context():
            # Get the SQL query
            from sqlalchemy.dialects import postgresql
            query = Block.query.filter_by(is_active=True).statement
            sql_query = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
            print(f"SQL query: {sql_query}")
            
            # Execute the query
            try:
                blocks = Block.query.all()
                print(f"✅ Successfully queried Block model: {len(blocks)} records")
                
                if blocks:
                    sample = blocks[0]
                    print(f"Sample record: id={sample.id}, title='{sample.title}'")
                return True
            except Exception as e:
                print(f"❌ Failed to query Block model: {e}")
                return False
    except Exception as e:
        print(f"❌ Error in ORM query: {e}")
        return False

def fix_remaining_issues(engine):
    """Attempt to fix any remaining issues."""
    print("\nAttempting to fix any remaining issues...")
    
    try:
        # Check if 'блок' table exists
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'блок' not in tables:
            print("'блок' table does not exist, creating it...")
            with engine.begin() as conn:
                conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
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
            
            print("✅ Created 'блок' table")
        
        # Check the Block model
        try:
            from app import create_app, db
            from app.models import Block
            
            # Set the tablename explicitly
            if getattr(Block, '__tablename__', None) != 'блок':
                Block.__tablename__ = 'блок'
                print(f"Updated Block.__tablename__ to 'блок'")
        except Exception as e:
            print(f"❌ Could not update Block model: {e}")
        
        # Transfer data if needed
        if 'block' in tables and 'блок' in tables:
            try:
                with engine.begin() as conn:
                    conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
                    # Check if Latin table has data
                    result = conn.execute(text('SELECT COUNT(*) FROM "block"'))
                    latin_count = result.scalar()
                    
                    # Check if Cyrillic table has data
                    result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                    cyrillic_count = result.scalar()
                    
                    if latin_count > 0 and cyrillic_count == 0:
                        print(f"Latin 'block' table has {latin_count} records, transferring to 'блок'...")
                        conn.execute(text("""
                        INSERT INTO "блок" (
                            id, title, content, image, "order", is_active, slug, is_top,
                            title_ua, title_en, title_de, title_ru,
                            content_ua, content_en, content_de, content_ru
                        )
                        SELECT 
                            id, title, content, image, "order", is_active, slug, is_top,
                            title_ua, title_en, title_de, title_ru,
                            content_ua, content_en, content_de, content_ru
                        FROM "block"
                        ON CONFLICT (id) DO NOTHING
                        """))
                        print("✅ Transferred data from 'block' to 'блок'")
            except Exception as e:
                print(f"❌ Error transferring data: {e}")
    
    except Exception as e:
        print(f"❌ Error fixing issues: {e}")

def verify_database_tables():
    """Comprehensive verification of database tables."""
    print("=" * 60)
    print("COMPREHENSIVE DATABASE TABLE VERIFICATION")
    print("=" * 60)
    
    # Get database URL
    db_url = get_database_url()
    if not db_url:
        return False
    
    # Check database connection
    engine = check_database_connection(db_url)
    if not engine:
        return False
    
    # Check tables
    tables_info = check_tables_in_database(engine)
    
    # Test queries
    query_success = check_queries(engine)
    
    # Test ORM queries
    orm_success = check_orm_query()
    
    # If any issues, try to fix them
    if not tables_info.get('cyrillic_block') or not query_success or not orm_success:
        fix_remaining_issues(engine)
        
        # Re-check after fixes
        tables_info = check_tables_in_database(engine)
        query_success = check_queries(engine)
        orm_success = check_orm_query()
    
    # Generate a summary
    success = tables_info.get('cyrillic_block') and query_success and orm_success
    
    print("\n" + "=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    print(f"Cyrillic 'блок' table exists: {tables_info.get('cyrillic_block')}")
    print(f"Direct SQL queries work: {query_success}")
    print(f"ORM queries work: {orm_success}")
    print(f"Overall success: {success}")
    
    # Save diagnostic results to a file for reference
    diagnostics = {
        'tables_info': tables_info,
        'query_success': query_success,
        'orm_success': orm_success,
        'overall_success': success
    }
    
    with open('database_diagnostics.json', 'w') as f:
        json.dump(diagnostics, f, indent=2, default=str)
    
    print("\nDetailed diagnostics saved to database_diagnostics.json")
    
    return success

if __name__ == "__main__":
    success = verify_database_tables()
    
    if success:
        print("\n✅ DATABASE VERIFICATION COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n⚠️ DATABASE VERIFICATION COMPLETED WITH ISSUES!")
        sys.exit(1)
