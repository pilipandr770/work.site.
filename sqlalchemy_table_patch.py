#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SQLAlchemy Monkey Patch for Table Names
This script monkey patches SQLAlchemy to handle both Cyrillic and Latin table names.
"""

import os
import sys
from sqlalchemy.sql.compiler import SQLCompiler

def apply_sqlalchemy_patch():
    """Apply a monkey patch to SQLAlchemy to handle table name issues."""
    print("=" * 60)
    print("SQLALCHEMY TABLE NAME MONKEY PATCH")
    print("=" * 60)
    
    try:
        # Import SQLAlchemy components for patching
        from sqlalchemy.sql import compiler
        from sqlalchemy import Table
        from sqlalchemy.sql.expression import TableClause
        
        # Store original methods
        original_visit_table = compiler.SQLCompiler.visit_table
        original_visit_tableclause = compiler.SQLCompiler.visit_tableclause
        
        # Create patched methods
        def patched_visit_table(self, table, asfrom=False, iscrud=False, **kwargs):
            """Patched method to handle both Cyrillic and Latin table names."""
            # Handle 'блок' table specially
            if table.name == 'блок' or table.name == 'block':
                print(f"Intercepted table name: {table.name}")
                # Try to use table name with quotes to preserve case/characters
                try:
                    # Use quoted name for exact representation
                    name = self.preparer.quote(table.name)
                    return name
                except Exception as e:
                    print(f"Error in table name quoting: {e}")
            
            # Fall back to original method
            return original_visit_table(self, table, asfrom, iscrud, **kwargs)
        
        def patched_visit_tableclause(self, table, iscrud=False, **kwargs):
            """Patched method to handle TableClause with Cyrillic names."""
            # Handle 'блок' table specially
            if table.name == 'блок' or table.name == 'block':
                print(f"Intercepted tableclause: {table.name}")
                name = self.preparer.quote(table.name)
                return name
            
            # Fall back to original method
            return original_visit_tableclause(self, table, iscrud, **kwargs)
        
        # Apply patches
        print("Applying SQLAlchemy compiler patches...")
        compiler.SQLCompiler.visit_table = patched_visit_table
        compiler.SQLCompiler.visit_tableclause = patched_visit_tableclause
        
        print("✅ SQLAlchemy monkey patch applied")
        
        # Test patch with app context
        try:
            from app import create_app, db
            from app.models import Block
            
            # Create app context
            app = create_app()
            with app.app_context():
                # Set Block.__tablename__ to Cyrillic for testing
                Block.__tablename__ = 'блок'
                
                # Generate a test query
                print("\nTesting SQL generation with monkey patch...")
                from sqlalchemy.dialects import postgresql
                query = Block.query.filter_by(is_active=True).statement
                sql = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
                
                print(f"Generated SQL with patch: {sql}")
                
                # Try executing the query
                try:
                    blocks = Block.query.all()
                    print(f"✅ Query successful! Found {len(blocks)} blocks.")
                    
                    if blocks:
                        print(f"First block: id={blocks[0].id}, title={blocks[0].title}")
                    
                    return True
                except Exception as e:
                    print(f"❌ Query execution failed: {e}")
                    return False
        
        except Exception as e:
            print(f"❌ Error testing patch: {e}")
            return False
    
    except Exception as e:
        print(f"❌ Error applying SQLAlchemy patch: {e}")
        return False

if __name__ == "__main__":
    success = apply_sqlalchemy_patch()
    
    if success:
        print("\n✅ SQLALCHEMY PATCH APPLIED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ SQLALCHEMY PATCH FAILED!")
        sys.exit(1)
