#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database Health Monitor for Render.com
This script checks the health of the PostgreSQL database connection
and reports any issues it finds.
"""

import os
import sys
import time
from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

def setup_environment():
    """Set up environment variables."""
    # Add the current directory to Python path
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.insert(0, str(current_dir))
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        env_path = current_dir / '.env'
        if env_path.exists():
            load_dotenv(env_path)
    except ImportError:
        pass

def check_database_health():
    """Check the health of the database connection."""
    print("\n=== DATABASE HEALTH CHECK ===\n")
    
    # Check for DATABASE_URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment")
        return False
    
    # Format the database URL for display
    masked_url = db_url
    if '@' in masked_url:
        parts = masked_url.split('@')
        auth = parts[0].split('://')
        masked_url = f"{auth[0]}://****:****@{parts[1]}"
    print(f"Database URL: {masked_url}")
    
    # Ensure correct URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    try:
        # Try to connect to the database
        print("Connecting to database...")
        engine = create_engine(db_url)
        start_time = time.time()
        
        with engine.connect() as conn:
            # Check connection latency
            conn_time = time.time() - start_time
            print(f"Connection established in {conn_time:.2f} seconds")
            
            # Get database info
            result = conn.execute(text("SELECT version(), current_database(), current_user"))
            row = result.fetchone()
            print(f"PostgreSQL version: {row[0].split(',')[0]}")
            print(f"Current database: {row[1]}")
            print(f"Current user: {row[2]}")
            
            # Check for tables
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Found {len(tables)} tables: {', '.join(tables[:5])}" + 
                  (f"... and {len(tables)-5} more" if len(tables) > 5 else ""))
            
            # Check for critical tables
            critical_tables = ['block', 'user', 'product', 'category']
            missing = [t for t in critical_tables if t not in tables]
            
            if missing:
                print(f"❌ Missing critical tables: {', '.join(missing)}")
            else:
                print("✅ All critical tables present")
            
            # Test queries on important tables
            try:
                user_count = conn.execute(text("SELECT COUNT(*) FROM \"user\"")).scalar()
                print(f"User count: {user_count}")
                
                admin_count = conn.execute(text("SELECT COUNT(*) FROM \"user\" WHERE is_admin = true")).scalar()
                print(f"Admin count: {admin_count}")
                
                if 'block' in tables:
                    block_count = conn.execute(text("SELECT COUNT(*) FROM block")).scalar()
                    print(f"Block count: {block_count}")
                
                print("✅ Test queries executed successfully")
            except SQLAlchemyError as e:
                print(f"❌ Error executing test queries: {e}")
        
        # Performance test
        print("\nRunning performance test...")
        start_time = time.time()
        with engine.connect() as conn:
            for _ in range(5):
                conn.execute(text("SELECT 1"))
        perf_time = time.time() - start_time
        print(f"5 simple queries executed in {perf_time:.2f} seconds")
        
        print("\n✅ Database health check completed successfully")
        return True
        
    except SQLAlchemyError as e:
        print(f"❌ Database connection error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    setup_environment()
    success = check_database_health()
    
    if not success:
        sys.exit(1)
