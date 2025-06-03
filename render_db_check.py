#!/usr/bin/env python
# render_db_check.py

import os
import sys

def check_env_vars():
    """Check environment variables related to the database connection."""
    
    # Check if DATABASE_URL is set
    db_url = os.environ.get('DATABASE_URL')
    
    if not db_url:
        print("❌ ERROR: DATABASE_URL environment variable is not set!")
        print("   You need to set this on your Render.com service.")
        print("\n   Go to: Dashboard > Your Web Service > Environment > Add Environment Variable")
        return False
    
    # Safety check - don't print the full URL with credentials
    safe_url = db_url
    if '@' in safe_url:
        # Hide username/password in the URL for displaying
        parts = safe_url.split('@')
        protocol_and_auth = parts[0].split('://')
        safe_url = f"{protocol_and_auth[0]}://****:****@{parts[1]}"
    
    # Check if it's a localhost URL
    if 'localhost' in db_url or '127.0.0.1' in db_url:
        print(f"❌ ERROR: Your DATABASE_URL contains 'localhost' or '127.0.0.1': {safe_url}")
        print("   This won't work on Render.com!")
        print("   You need to use the PostgreSQL URL provided by Render.")
        print("\n   Go to: Dashboard > Your PostgreSQL > Connections > Internal Database URL")
        return False
    
    # Check if it's a PostgreSQL URL
    if not (db_url.startswith('postgresql://') or db_url.startswith('postgres://')):
        print(f"❌ ERROR: Your DATABASE_URL is not a PostgreSQL URL: {safe_url}")
        print("   It should start with 'postgresql://' or 'postgres://'")
        return False
    
    # All checks passed
    print(f"✅ DATABASE_URL environment variable is set and looks correct.")
    print(f"   URL Format: {safe_url}")
    return True

def check_render_environment():
    """Check if we're running on Render.com."""
    
    render_var = os.environ.get('RENDER')
    render_service = os.environ.get('RENDER_SERVICE_ID')
    
    if render_var or render_service:
        print("✅ Running on Render.com environment.")
        return True
    else:
        print("ℹ️ Not running on Render.com - this is a local environment.")
        return False

def main():
    print("\n=== RENDER DATABASE CONNECTION CHECKER ===\n")
    
    # Check if we're on Render
    on_render = check_render_environment()
    
    # Check DATABASE_URL environment variable
    db_url_ok = check_env_vars()
    
    if on_render and db_url_ok:
        print("\n✅ Your Render.com environment appears to be correctly configured for PostgreSQL!")
        print("   Your application should be able to connect to the database.")
    elif on_render and not db_url_ok:
        print("\n❌ Your Render.com environment is NOT correctly configured for PostgreSQL.")
        print("   Please fix the issues mentioned above.")
    elif not on_render:
        print("\nℹ️ Since you're running locally, make sure your .env file has either:")
        print("   1. A local PostgreSQL URL for development")
        print("   2. Or no DATABASE_URL to fall back to SQLite for development")
    
    print("\n=== CHECK COMPLETE ===\n")

if __name__ == "__main__":
    main()
