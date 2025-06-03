#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database Fix Verification
This script provides a final verification that our database solution is working correctly.
It displays important information about the current state of the database and application.
"""

import os
import sys
import json
import traceback
from datetime import datetime

def verify_database_solution():
    """Verify that our database solution is working correctly."""
    print("=" * 60)
    print("DATABASE FIX VERIFICATION")
    print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": {},
        "database": {},
        "models": {},
        "queries": {}
    }
    
    try:
        # Check environment
        print("Checking environment...")
        results["environment"]["DATABASE_URL"] = os.environ.get("DATABASE_URL", "Not set")
        results["environment"]["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS", "Not set")
        
        # Import app components
        from app import create_app, db
        from app.models import Block, User
        
        # Check Block model configuration
        print("\nChecking Block model configuration...")
        block_tablename = getattr(Block, "__tablename__", None)
        print(f"Block.__tablename__ = {block_tablename}")
        results["models"]["block_tablename"] = block_tablename
        
        # Create app with context
        app = create_app()
        
        # Check SQLAlchemy configuration
        print("\nChecking SQLAlchemy configuration...")
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "Not configured")
        print(f"SQLALCHEMY_DATABASE_URI = {db_uri[:10]}...{db_uri[-10:] if len(db_uri) > 20 else db_uri}")
        results["database"]["uri"] = db_uri
        
        with app.app_context():
            # Check tables in database
            print("\nChecking database tables...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Tables in database: {', '.join(tables)}")
            results["database"]["tables"] = tables
            
            # Check specific tables
            if "block" in tables:
                print("✅ 'block' table exists")
                results["database"]["block_table_exists"] = True
                
                # Get table columns
                columns = [c["name"] for c in inspector.get_columns("block")]
                print(f"'block' table columns: {columns}")
                results["database"]["block_columns"] = columns
            else:
                print("❌ 'block' table does not exist")
                results["database"]["block_table_exists"] = False
            
            if "блок" in tables:
                print("✅ 'блок' table exists")
                results["database"]["cyrillic_block_table_exists"] = True
            else:
                print("❌ 'блок' table does not exist")
                results["database"]["cyrillic_block_table_exists"] = False
            
            # Test direct SQL queries
            print("\nTesting direct SQL queries...")
            from sqlalchemy import text
            
            try:
                with db.engine.connect() as conn:
                    # Test Latin block table
                    result = conn.execute(text("SELECT COUNT(*) FROM block"))
                    count = result.scalar()
                    print(f"✅ Direct query to 'block' table: {count} records")
                    results["queries"]["direct_block_count"] = count
            except Exception as e:
                print(f"❌ Direct query to 'block' table failed: {e}")
                results["queries"]["direct_block_error"] = str(e)
            
            # Test ORM queries
            print("\nTesting ORM queries...")
            try:
                block_count = Block.query.count()
                print(f"✅ Block.query.count() = {block_count}")
                results["queries"]["orm_block_count"] = block_count
                
                # Get the SQL for a Block query
                query = Block.query.filter_by(is_active=True).statement
                from sqlalchemy.dialects import postgresql
                sql = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
                print(f"Generated SQL: {sql}")
                results["queries"]["generated_sql"] = sql
                
                # Try to fetch a Block
                block = Block.query.first()
                if block:
                    print(f"✅ Successfully fetched Block: id={block.id}, title={block.title}")
                    results["queries"]["block_fetch"] = {"id": block.id, "title": block.title}
                else:
                    print("ℹ️ No Block records found, but query worked")
                    results["queries"]["block_fetch"] = None
            except Exception as e:
                print(f"❌ Block ORM query failed: {e}")
                traceback.print_exc()
                results["queries"]["orm_block_error"] = str(e)
        
        # Try to create a Block
        print("\nTrying to create a Block...")
        with app.app_context():
            try:
                new_block = Block(
                    title="Test Block",
                    content="This is a test block created by the verification script.",
                    slug="test-block",
                    is_active=True,
                    is_top=False
                )
                db.session.add(new_block)
                db.session.commit()
                print(f"✅ Successfully created Block: id={new_block.id}")
                results["queries"]["block_create"] = {"id": new_block.id}
            except Exception as e:
                print(f"❌ Block creation failed: {e}")
                traceback.print_exc()
                results["queries"]["block_create_error"] = str(e)
        
        # Save the results
        with open("database_fix_verification.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("\nDetailed results saved to database_fix_verification.json")
        
        # Final verdict
        block_table_exists = results["database"].get("block_table_exists", False)
        orm_queries_work = "orm_block_error" not in results["queries"]
        block_creation_works = "block_create_error" not in results["queries"]
        
        success = block_table_exists and orm_queries_work and block_creation_works
        
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Block table exists: {'✅' if block_table_exists else '❌'}")
        print(f"ORM queries work: {'✅' if orm_queries_work else '❌'}")
        print(f"Block creation works: {'✅' if block_creation_works else '❌'}")
        print(f"\nOverall success: {'✅' if success else '❌'}")
        
        return success
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_database_solution()
    
    if success:
        print("\n✅ DATABASE FIX VERIFICATION PASSED!")
        sys.exit(0)
    else:
        print("\n❌ DATABASE FIX VERIFICATION FAILED!")
        sys.exit(1)
