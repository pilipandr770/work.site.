#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct App Creation Test
This script directly tests the app creation and database initialization.
"""

import os
import sys
import traceback

def test_app_creation():
    """Test app creation and database initialization."""
    print("=" * 60)
    print("DIRECT APP CREATION TEST")
    print("=" * 60)
    
    try:
        print("Importing app components...")
        from app import create_app, db
        
        print("Creating Flask app...")
        app = create_app()
        
        print("App created successfully!")
        print(f"SQLAlchemy database URI: {app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')}")
        
        # Further database checks
        with app.app_context():
            # Import models
            from app.models import Block, User
            
            # Print tablenames
            block_tablename = getattr(Block, '__tablename__', None)
            user_tablename = getattr(User, '__tablename__', None)
            
            print(f"Block.__tablename__ = {block_tablename}")
            print(f"User.__tablename__ = {user_tablename}")
            
            # Check tables in database
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"Tables in database: {', '.join(tables)}")
            
            # Check if block tables exist
            if 'block' in tables:
                print("✅ 'block' table exists")
            else:
                print("❌ 'block' table does not exist")
                
            if 'блок' in tables:
                print("✅ 'блок' table exists")
            else:
                print("❌ 'блок' table does not exist")
            
            # Try querying Block model
            try:
                count = Block.query.count()
                print(f"✅ Block query successful with {count} records")
                
                # Try to fetch one record
                block = Block.query.first()
                if block:
                    print(f"✅ First block: id={block.id}, title={block.title}")
                else:
                    print("ℹ️ No Block records found, but query worked")
            except Exception as e:
                print(f"❌ Block query failed: {e}")
                traceback.print_exc()
        
        return True
    except Exception as e:
        print(f"❌ Error testing app creation: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_app_creation()
    
    if success:
        print("\n✅ App creation test completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ App creation test failed!")
        sys.exit(1)
