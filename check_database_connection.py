#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Database Connection Parameter Check
This script checks the database connection parameters and verifies that they're valid.
It also tests the connection with different encoding settings.
"""

import os
import sys
import json
import urllib.parse

def check_database_parameters():
    """Check and validate database connection parameters."""
    print("=" * 60)
    print("DATABASE CONNECTION PARAMETER CHECK")
    print("=" * 60)
    
    # Get database URL
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables!")
        return False
    
    print(f"Original DATABASE_URL: {db_url[:10]}...{db_url[-10:]} (partially hidden for security)")
    
    # Fix for PostgreSQL URL format
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
        print("ℹ️ Converted 'postgres://' to 'postgresql://'")
    
    # Parse database URL
    try:
        parsed = urllib.parse.urlparse(db_url)
        
        # Extract components
        db_params = {
            'scheme': parsed.scheme,
            'username': parsed.username,
            'password': '********' if parsed.password else None,
            'hostname': parsed.hostname,
            'port': parsed.port,
            'path': parsed.path,
            'dbname': parsed.path[1:] if parsed.path else None
        }
        
        print("\nDatabase Parameters:")
        print(f"- Scheme: {db_params['scheme']}")
        print(f"- Username: {db_params['username']}")
        print(f"- Password: {'Set' if db_params['password'] else 'Not set'}")
        print(f"- Hostname: {db_params['hostname']}")
        print(f"- Port: {db_params['port']}")
        print(f"- Database Name: {db_params['dbname']}")
    except Exception as e:
        print(f"❌ Error parsing DATABASE_URL: {e}")
        return False
    
    # Test connection with SQLAlchemy
    print("\nTesting connection with SQLAlchemy...")
    try:
        from sqlalchemy import create_engine, text
        
        # Test with default settings
        print("Connecting with default settings...")
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.scalar()
            print(f"✅ Connected successfully! PostgreSQL version: {version}")
            
            # Test with UTF-8 encoding
            print("\nTesting UTF-8 encoding...")
            conn.execute(text("SET CLIENT_ENCODING TO 'UTF8'"))
            result = conn.execute(text("SHOW client_encoding"))
            encoding = result.scalar()
            print(f"Client encoding: {encoding}")
            
            # Try to create a table with Cyrillic name
            print("\nTesting Cyrillic table creation...")
            conn.execute(text('DROP TABLE IF EXISTS "тест" CASCADE'))
            conn.execute(text('CREATE TABLE "тест" (id SERIAL PRIMARY KEY, name VARCHAR(64))'))
            conn.execute(text('INSERT INTO "тест" (name) VALUES (\'тестовая запись\')'))
            result = conn.execute(text('SELECT COUNT(*) FROM "тест"'))
            count = result.scalar()
            print(f"✅ Created Cyrillic test table and inserted {count} record(s)")
            
            # Check available tables
            print("\nListing all tables...")
            result = conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result]
            print(f"Tables in database: {', '.join(tables)}")
            
            # Check if блок table exists
            if 'блок' in tables:
                print("✅ 'блок' table exists")
                # Check its structure
                result = conn.execute(text("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = 'блок'
                    ORDER BY ordinal_position
                """))
                columns = [(row[0], row[1]) for row in result]
                print(f"'блок' table columns: {json.dumps(columns, indent=2)}")
            else:
                print("❌ 'блок' table does not exist")
        
        # Save connection details for reference
        connection_details = {
            'db_params': db_params,
            'tables': tables,
            'encoding': encoding,
            'version': version,
        }
        
        with open('database_connection_details.json', 'w') as f:
            json.dump(connection_details, f, indent=2)
        
        print("\nConnection details saved to database_connection_details.json")
        return True
    except Exception as e:
        print(f"❌ Error testing connection: {e}")
        return False

if __name__ == "__main__":
    success = check_database_parameters()
    
    if success:
        print("\n✅ DATABASE CONNECTION CHECK COMPLETED SUCCESSFULLY!")
        sys.exit(0)
    else:
        print("\n❌ DATABASE CONNECTION CHECK FAILED!")
        sys.exit(1)
