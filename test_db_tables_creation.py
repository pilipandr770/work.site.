#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test Database Table Creation
This script tests whether the database tables are created correctly when the app is initialized.
"""

import os
import sys

def test_db_creation():
    """Test that database tables are created correctly."""
    print("=" * 60)
    print("DATABASE TABLE CREATION TEST")
    print("=" * 60)
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block, User
        
        print("Creating app with app context...")
        app = create_app()
        
        # Check database tables
        with app.app_context():
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            
            # Get all tables
            all_tables = inspector.get_table_names()
            print(f"All tables in database: {', '.join(all_tables)}")
            
            # Check for specific tables
            critical_tables = ['block', 'блок', 'user', 'product', 'category']
            for table in critical_tables:
                if table in all_tables:
                    print(f"✅ Table '{table}' exists")
                else:
                    print(f"❌ Table '{table}' does not exist")
            
            # Try direct SQL queries
            try:
                from sqlalchemy import text
                with db.engine.connect() as conn:
                    # Set UTF-8 encoding
                    conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
                    
                    # Try querying Latin block table
                    try:
                        result = conn.execute(text('SELECT COUNT(*) FROM block'))
                        count = result.scalar()
                        print(f"✅ Can query 'block' table: {count} records")
                    except Exception as e:
                        print(f"❌ Cannot query 'block' table: {e}")
                    
                    # Try querying Cyrillic block table
                    try:
                        result = conn.execute(text('SELECT COUNT(*) FROM "блок"'))
                        count = result.scalar()
                        print(f"✅ Can query 'блок' table: {count} records")
                    except Exception as e:
                        print(f"❌ Cannot query 'блок' table: {e}")
            except Exception as e:
                print(f"❌ Error executing SQL: {e}")
            
            # Try ORM queries
            try:
                blocks_count = Block.query.count()
                print(f"✅ Successfully queried Block model: {blocks_count} records")
            except Exception as e:
                print(f"❌ Cannot query Block model: {e}")
                
            return True
    except Exception as e:
        print(f"❌ Error testing database creation: {e}")
        return False

if __name__ == "__main__":
    success = test_db_creation()
    
    if success:
        print("\n✅ Database tables test completed!")
        sys.exit(0)
    else:
        print("\n❌ Database tables test failed!")
        sys.exit(1)
