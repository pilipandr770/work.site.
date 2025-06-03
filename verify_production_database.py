#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Production Database Verification
This script provides a final verification that our database solution is working correctly on production.
It can be run locally but simulates what happens when data is accessed on production.
"""

import os
import sys
import json
from datetime import datetime
import traceback

def verify_production_database():
    """Verify that our database solution is working correctly on production."""
    print("=" * 60)
    print("PRODUCTION DATABASE VERIFICATION")
    print("=" * 60)
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "environment": {},
        "database": {},
        "models": {},
        "checks": {}
    }
    
    try:
        # Import app components
        from app import create_app, db
        from app.models import Block
        
        # Check Block model configuration
        print("Checking Block model configuration...")
        block_tablename = getattr(Block, "__tablename__", None)
        print(f"Block.__tablename__ = {block_tablename}")
        results["models"]["block_tablename"] = block_tablename
        
        # Check that the tablename is explicit and Latin
        if block_tablename == "block":
            print("✅ Block model has correct explicit tablename 'block'")
            results["checks"]["explicit_tablename"] = True
        else:
            print(f"❌ Block model has incorrect tablename: '{block_tablename}'")
            results["checks"]["explicit_tablename"] = False
        
        # Create app with context
        app = create_app()
        
        # Check SQLAlchemy configuration
        print("\nChecking SQLAlchemy configuration...")
        db_uri = app.config.get("SQLALCHEMY_DATABASE_URI", "Not configured")
        masked_uri = db_uri[:10] + "..." + db_uri[-10:] if len(db_uri) > 20 else db_uri
        print(f"SQLALCHEMY_DATABASE_URI = {masked_uri}")
        results["database"]["uri_type"] = db_uri.split("://")[0] if "://" in db_uri else "unknown"
        
        with app.app_context():
            # Simulate what happens on application startup
            print("\nSimulating application startup...")
            
            # Check if db.create_all() is in create_app()
            from inspect import getsource
            from app import create_app as create_app_func
            
            source = getsource(create_app_func)
            if "db.create_all()" in source:
                print("✅ db.create_all() is present in create_app()")
                results["checks"]["db_create_all_present"] = True
            else:
                print("❌ db.create_all() is NOT present in create_app()")
                results["checks"]["db_create_all_present"] = False
            
            # Check Block query functionality
            print("\nTesting Block querying...")
            try:
                # Generate the SQL query to test how SQLAlchemy handles the table name
                query = Block.query.filter_by(is_active=True).statement
                from sqlalchemy.dialects import postgresql
                sql = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
                print(f"Generated SQL: {sql}")
                
                # Check if SQL references 'block' instead of 'блок'
                if "FROM block" in sql and "FROM блок" not in sql:
                    print("✅ SQL query references 'block' table (Latin)")
                    results["checks"]["sql_uses_latin_table"] = True
                else:
                    print("❌ SQL query does not use Latin table name")
                    results["checks"]["sql_uses_latin_table"] = False
                
                results["checks"]["generated_sql"] = sql
                
                # Try to execute a query (this will fail if the table doesn't exist)
                blocks = Block.query.all()
                print(f"✅ Successfully queried Block table: {len(blocks)} records found")
                results["checks"]["query_success"] = True
            except Exception as e:
                print(f"❌ Block query failed: {e}")
                traceback.print_exc()
                results["checks"]["query_error"] = str(e)
                results["checks"]["query_success"] = False
        
        # Save the results
        with open("production_database_verification.json", "w") as f:
            json.dump(results, f, indent=2, default=str)
        print("\nDetailed results saved to production_database_verification.json")
        
        # Final verdict
        explicit_tablename = results["checks"].get("explicit_tablename", False)
        db_create_all_present = results["checks"].get("db_create_all_present", False)
        sql_uses_latin_table = results["checks"].get("sql_uses_latin_table", False)
        query_success = results["checks"].get("query_success", False)
        
        success = explicit_tablename and db_create_all_present and sql_uses_latin_table and query_success
        
        print("\n" + "=" * 60)
        print("VERIFICATION SUMMARY")
        print("=" * 60)
        print(f"Block model has explicit 'block' tablename: {'✅' if explicit_tablename else '❌'}")
        print(f"db.create_all() is present in create_app(): {'✅' if db_create_all_present else '❌'}")
        print(f"SQL queries reference 'block' table (Latin): {'✅' if sql_uses_latin_table else '❌'}")
        print(f"Block query successful: {'✅' if query_success else '❌'}")
        print(f"\nOverall success: {'✅' if success else '❌'}")
        
        return success
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = verify_production_database()
    
    if success:
        print("\n✅ PRODUCTION DATABASE VERIFICATION PASSED!")
        sys.exit(0)
    else:
        print("\n❌ PRODUCTION DATABASE VERIFICATION FAILED!")
        sys.exit(1)
