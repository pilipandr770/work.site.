#!/usr/bin/env python
# check_render_postgres.py
import os
import sys
import time
from urllib.parse import urlparse

def check_database_url():
    """Check if DATABASE_URL is set and properly formatted."""
    
    # Get DATABASE_URL environment variable
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("ERROR: DATABASE_URL environment variable is not set!")
        print("Please set DATABASE_URL in your render.com environment variables.")
        return False
    
    # Check if it's a PostgreSQL URL
    if not (db_url.startswith('postgresql://') or db_url.startswith('postgres://')):
        print(f"ERROR: DATABASE_URL is not a PostgreSQL URL: {db_url}")
        print("It should start with 'postgresql://' or 'postgres://'")
        return False
    
    # Check if it contains localhost, which won't work on render.com
    if 'localhost' in db_url or '127.0.0.1' in db_url:
        print("ERROR: DATABASE_URL contains 'localhost' or '127.0.0.1'!")
        print("This won't work on render.com! You need to use a hosted PostgreSQL database.")
        print(f"Current value: {db_url}")
        return False
        
    try:
        # Parse URL to check components
        parsed = urlparse(db_url)
        
        if not parsed.hostname:
            print("ERROR: No hostname in DATABASE_URL")
            return False
            
        if not parsed.username:
            print("WARNING: No username in DATABASE_URL")
            
        if not parsed.path or parsed.path == '/':
            print("ERROR: No database name in DATABASE_URL")
            return False
        
        print("DATABASE_URL format looks valid.")
        return True
        
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}")
        return False

def attempt_postgres_connection():
    """Attempt to connect to the PostgreSQL database."""
    try:
        import psycopg2
        from psycopg2 import OperationalError
        
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print("No DATABASE_URL set. Cannot attempt connection.")
            return False
            
        print("Attempting to connect to PostgreSQL...")
        
        # Try to connect to the database
        conn = psycopg2.connect(db_url)
        
        # If successful
        print("✅ Successfully connected to PostgreSQL database!")
        
        # Check server version
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL server info: {version}")
        
        # List tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        if tables:
            print("\nAvailable tables:")
            for table in tables:
                print(f"- {table[0]}")
        else:
            print("\nNo tables found in database. You may need to run migrations.")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("ERROR: psycopg2 module not installed! Run: pip install psycopg2-binary")
        return False
    except OperationalError as e:
        print(f"ERROR: Could not connect to PostgreSQL database: {e}")
        return False
    except Exception as e:
        print(f"ERROR: Unexpected error when connecting to database: {e}")
        return False

def main():
    """Main function to check database setup."""
    
    print("======= DATABASE CONFIGURATION CHECK =======")
    print(f"Environment: {'PRODUCTION' if os.environ.get('RENDER') else 'DEVELOPMENT'}")
    print(f"Python version: {sys.version}")
    print("")
    
    # Check DATABASE_URL format
    url_valid = check_database_url()
    
    if not url_valid:
        print("\n⚠️  Please fix your DATABASE_URL before continuing!")
        return
    
    # Try connecting to PostgreSQL
    connection_success = attempt_postgres_connection()
    
    if connection_success:
        print("\n✅ Database configuration appears correct!")
    else:
        print("\n⚠️  Database connection failed. Please check your configuration.")

if __name__ == "__main__":
    main()
