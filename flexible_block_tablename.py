#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runtime Block Model Dual Tablename Patch
This script modifies the Block model at runtime to try both Cyrillic and Latin table names.
"""

import os
import sys
from functools import wraps

def flexible_tablename_patch():
    """Create a runtime patch for Block model to support multiple table names."""
    print("=" * 60)
    print("FLEXIBLE TABLE NAME PATCH")
    print("=" * 60)
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block
        from sqlalchemy.ext.declarative import declared_attr
        
        # Save original query method
        original_query = db.Query
        
        # Create a flexible query class that tries both table names
        class FlexibleQuery(db.Query):
            def __init__(self, *args, **kwargs):
                super(FlexibleQuery, self).__init__(*args, **kwargs)
            
            def _try_with_tablename(self, func_name, *args, **kwargs):
                # Try with current tablename first
                try:
                    method = getattr(super(FlexibleQuery, self), func_name)
                    result = method(*args, **kwargs)
                    return result
                except Exception as e1:
                    # If that fails, try the alternative tablename
                    print(f"Query with current tablename failed: {e1}")
                    
                    # Switch tablename
                    original_tablename = getattr(self._primary_entity.entity_zero().entity, '__tablename__', None)
                    if original_tablename == 'блок':
                        new_tablename = 'block'
                    else:
                        new_tablename = 'блок'
                    
                    print(f"Trying with alternate tablename: {new_tablename}")
                    self._primary_entity.entity_zero().entity.__tablename__ = new_tablename
                    
                    try:
                        method = getattr(super(FlexibleQuery, self), func_name)
                        result = method(*args, **kwargs)
                        return result
                    except Exception as e2:
                        print(f"Query with alternate tablename failed: {e2}")
                        # If both fail, re-raise the original exception
                        raise e1
            
            def all(self, *args, **kwargs):
                return self._try_with_tablename('all', *args, **kwargs)
                
            def first(self, *args, **kwargs):
                return self._try_with_tablename('first', *args, **kwargs)
                
            def one(self, *args, **kwargs):
                return self._try_with_tablename('one', *args, **kwargs)
                
            def one_or_none(self, *args, **kwargs):
                return self._try_with_tablename('one_or_none', *args, **kwargs)
        
        # Patch the Block model
        print("Patching Block model...")
        
        # Create a dual-table capable Block model
        class DualNamedBlock:
            @declared_attr
            def __tablename__(cls):
                # Try both table names
                from sqlalchemy import inspect
                engine = db.get_engine()
                insp = inspect(engine)
                
                if 'блок' in insp.get_table_names():
                    print("Using Cyrillic 'блок' table name")
                    return 'блок'
                elif 'block' in insp.get_table_names():
                    print("Using Latin 'block' table name")
                    return 'block'
                else:
                    print("No block table found, defaulting to Cyrillic 'блок'")
                    return 'блок'
        
        # Apply the patches
        db.Query = FlexibleQuery
        Block.__tablename__ = 'блок'  # Start with Cyrillic name
        
        # Test the patch
        app = create_app()
        with app.app_context():
            try:
                # Test query
                print("\nTesting flexible Block query...")
                test_blocks = Block.query.all()
                print(f"✅ Query successful! Found {len(test_blocks)} blocks.")
                
                if test_blocks:
                    print(f"First block: id={test_blocks[0].id}, title={test_blocks[0].title}")
                
                return True
            except Exception as e:
                print(f"❌ Test query failed: {e}")
                return False
    
    except Exception as e:
        print(f"❌ Error patching model: {e}")
        return False

if __name__ == "__main__":
    success = flexible_tablename_patch()
    
    if success:
        print("\n✅ FLEXIBLE TABLE NAME PATCH APPLIED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ FLEXIBLE TABLE NAME PATCH FAILED!")
        sys.exit(1)
