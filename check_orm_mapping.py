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
            # Get table name from model
            block_tablename = Block.__tablename__
            print(f"Block model __tablename__: {block_tablename}")
            
            # Get table name in database
            engine = db.engine
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {', '.join(tables)}")
            
            # Check if there's a mismatch
            if block_tablename not in tables and 'block' in tables:
                print("⚠️ Detected tablename mismatch!")
                print(f"Model expects '{block_tablename}' but database has 'block'")
                
                # Try to fix by creating a view
                try:
                    with engine.begin() as conn:
                        conn.execute(text(f"""
                        CREATE OR REPLACE VIEW "{block_tablename}" AS SELECT * FROM block;
                        """))
                    print(f"✅ Created view '{block_tablename}' pointing to 'block' table")
                except Exception as e:
                    print(f"❌ Failed to create view: {e}")
            
            # Try querying through the ORM
            try:
                blocks_count = Block.query.count()
                print(f"✅ Successfully queried Block model: {blocks_count} records")
                return True
            except Exception as e:
                print(f"❌ Failed to query Block model: {e}")
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
