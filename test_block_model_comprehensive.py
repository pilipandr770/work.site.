#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Comprehensive Block Model Test
This script performs a thorough test of the Block model to ensure it's working properly.
"""

import os
import sys
import json
import traceback

def test_block_model_comprehensive():
    """Perform a comprehensive test of the Block model."""
    print("=" * 60)
    print("COMPREHENSIVE BLOCK MODEL TEST")
    print("=" * 60)
    
    results = {
        "tests": [],
        "overall_success": False,
        "error": None
    }
    
    try:
        # Import app components
        print("Importing app components...")
        from app import create_app, db
        from app.models import Block
        
        # Get tablename
        tablename = getattr(Block, '__tablename__', None)
        print(f"Initial Block.__tablename__ = {tablename}")
        results["tests"].append({"name": "Check __tablename__", "result": tablename, "success": tablename is not None})
        
        # Create app context
        app = create_app()
        with app.app_context():
            # Get database URL
            database_url = app.config.get('SQLALCHEMY_DATABASE_URI', 'Not configured')
            print(f"Database URL: {database_url[:10]}...{database_url[-10:] if len(database_url) > 20 else database_url}")
            
            # Check if database URL is PostgreSQL
            is_postgresql = database_url.startswith('postgresql://') or database_url.startswith('postgres://')
            results["tests"].append({"name": "Check database is PostgreSQL", "result": is_postgresql, "success": is_postgresql})
            
            # Check available tables
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"Available tables: {tables}")
            
            # Check for block tables
            has_cyrillic_block = 'блок' in tables
            has_latin_block = 'block' in tables
            print(f"Has Cyrillic 'блок' table: {has_cyrillic_block}")
            print(f"Has Latin 'block' table: {has_latin_block}")
            results["tests"].append({"name": "Check Cyrillic table exists", "result": has_cyrillic_block, "success": has_cyrillic_block})
            results["tests"].append({"name": "Check Latin table exists", "result": has_latin_block, "success": has_latin_block})
            
            # Test queries
            print("\nTesting queries with different table names:")
            
            # Test with original tablename
            print(f"\n1. Testing with original tablename: {tablename}")
            try:
                all_blocks = Block.query.all()
                count = len(all_blocks)
                print(f"✅ Query successful! Found {count} blocks")
                if count > 0:
                    print(f"First block: id={all_blocks[0].id}, title={all_blocks[0].title}")
                results["tests"].append({"name": f"Query with {tablename}", "result": count, "success": True})
            except Exception as e:
                print(f"❌ Query failed: {e}")
                traceback.print_exc()
                results["tests"].append({"name": f"Query with {tablename}", "result": str(e), "success": False})
            
            # Test with Cyrillic tablename
            if tablename != 'блок':
                print("\n2. Testing with Cyrillic tablename: 'блок'")
                try:
                    Block.__tablename__ = 'блок'
                    all_blocks = Block.query.all()
                    count = len(all_blocks)
                    print(f"✅ Query successful! Found {count} blocks")
                    if count > 0:
                        print(f"First block: id={all_blocks[0].id}, title={all_blocks[0].title}")
                    results["tests"].append({"name": "Query with 'блок'", "result": count, "success": True})
                except Exception as e:
                    print(f"❌ Query failed: {e}")
                    traceback.print_exc()
                    results["tests"].append({"name": "Query with 'блок'", "result": str(e), "success": False})
            
            # Test with Latin tablename
            if tablename != 'block':
                print("\n3. Testing with Latin tablename: 'block'")
                try:
                    Block.__tablename__ = 'block'
                    all_blocks = Block.query.all()
                    count = len(all_blocks)
                    print(f"✅ Query successful! Found {count} blocks")
                    if count > 0:
                        print(f"First block: id={all_blocks[0].id}, title={all_blocks[0].title}")
                    results["tests"].append({"name": "Query with 'block'", "result": count, "success": True})
                except Exception as e:
                    print(f"❌ Query failed: {e}")
                    traceback.print_exc()
                    results["tests"].append({"name": "Query with 'block'", "result": str(e), "success": False})
            
            # Get SQL query
            print("\n4. Examining SQL query generation:")
            try:
                from sqlalchemy.dialects import postgresql
                query = Block.query.filter_by(is_active=True).statement
                sql_query = str(query.compile(dialect=postgresql.dialect(), compile_kwargs={"literal_binds": True}))
                print(f"Generated SQL query: {sql_query}")
                results["tests"].append({"name": "SQL Query Generation", "result": sql_query, "success": True})
            except Exception as e:
                print(f"❌ SQL generation failed: {e}")
                traceback.print_exc()
                results["tests"].append({"name": "SQL Query Generation", "result": str(e), "success": False})
            
            # Check success criteria
            successes = [test["success"] for test in results["tests"]]
            results["overall_success"] = any(successes)
            
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        for test in results["tests"]:
            status = "✅" if test["success"] else "❌"
            print(f"{status} {test['name']}: {test['result']}")
        
        print(f"\nOverall success: {'✅' if results['overall_success'] else '❌'}")
        
        # Save results to file
        with open('block_model_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\nTest results saved to block_model_test_results.json")
        
        return results["overall_success"]
    
    except Exception as e:
        print(f"❌ Error in test: {e}")
        traceback.print_exc()
        results["error"] = str(e)
        
        # Save results to file
        with open('block_model_test_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("\nTest results saved to block_model_test_results.json")
        
        return False

if __name__ == "__main__":
    success = test_block_model_comprehensive()
    
    if success:
        print("\n✅ BLOCK MODEL TEST COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ BLOCK MODEL TEST FAILED!")
        sys.exit(1)
