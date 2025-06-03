#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Reset Block Model Tablename
This script resets the Block model's __tablename__ attribute to ensure consistency.
"""

import os
import sys

def reset_block_tablename():
    """Reset the Block model's tablename attribute."""
    print("=" * 60)
    print("RESET BLOCK MODEL TABLENAME")
    print("=" * 60)
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block
        
        # Check current tablename
        current_tablename = getattr(Block, "__tablename__", None)
        print(f"Current Block.__tablename__ = {current_tablename}")
        
        # Modify tablename if needed
        if current_tablename != "block":
            Block.__tablename__ = "block"
            print(f"Block.__tablename__ reset to 'block'")
        else:
            print("Block.__tablename__ is already 'block'")
        
        # Create app context and check
        app = create_app()
        with app.app_context():
            # Check tables in database
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if "block" in tables:
                print("✅ 'block' table exists in database")
            else:
                print("❌ 'block' table does not exist in database")
                
                # Create the table if it doesn't exist
                print("Creating 'block' table...")
                Block.__table__.create(db.engine)
                print("✅ 'block' table created")
            
            # Test query
            try:
                count = Block.query.count()
                print(f"✅ Block.query.count() = {count}")
                return True
            except Exception as e:
                print(f"❌ Block.query.count() failed: {e}")
                return False
    except Exception as e:
        print(f"❌ Error resetting Block tablename: {e}")
        return False

if __name__ == "__main__":
    success = reset_block_tablename()
    
    if success:
        print("\n✅ BLOCK MODEL TABLENAME RESET SUCCESSFUL!")
        sys.exit(0)
    else:
        print("\n❌ BLOCK MODEL TABLENAME RESET FAILED!")
        sys.exit(1)
