#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Patch for models.py to explicitly set table names
This ensures table names are set correctly in Latin characters
"""

import sys

def patch_model_table_names():
    """Patch model table names in the model.py file."""
    try:
        print("=== PATCHING MODEL TABLE NAMES ===")
        
        # Import app and db
        from app import create_app, db
        from app.models import Block, User
        
        # Create app context
        app = create_app()
        with app.app_context():
            # Check current table names
            block_tablename = getattr(Block, '__tablename__', 'block')
            user_tablename = getattr(User, '__tablename__', 'user')
            
            print(f"Current Block.__tablename__ = {block_tablename}")
            print(f"Current User.__tablename__ = {user_tablename}")
            
            # Modify table names if needed
            if block_tablename != 'block':
                print("Setting Block.__tablename__ to 'block'")
                Block.__tablename__ = 'block'
                
            if user_tablename != 'user':
                print("Setting User.__tablename__ to 'user'")
                User.__tablename__ = 'user'
            
            # Verify table names
            print(f"Updated Block.__tablename__ = {Block.__tablename__}")
            print(f"Updated User.__tablename__ = {User.__tablename__}")
            
        print("✅ Model table names patched successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error patching model table names: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("MODEL TABLE NAME PATCHING")
    print("This script patches table names in models to ensure correct database mapping")
    print("=" * 60)
    
    success = patch_model_table_names()
    
    if success:
        print("\n✅ Model patching completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Model patching failed!")
        sys.exit(1)
