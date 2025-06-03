#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Direct database initialization script for Render.com
This is a simplified script that directly creates database tables.
Use this if other methods fail.
"""

import sys
from sqlalchemy.exc import SQLAlchemyError

def main():
    try:
        print("=== DIRECT DATABASE INITIALIZATION ===")
        
        # Import app components
        try:
            print("Importing application modules...")
            from app import create_app, db
            from app.models import User, Block, Settings, Token, Category, Product
            from werkzeug.security import generate_password_hash
        except ImportError as e:
            print(f"Error importing modules: {e}")
            return False
        
        # Create app with context
        try:
            print("Creating application context...")
            app = create_app()
        except Exception as e:
            print(f"Error creating app: {e}")
            return False
        
        # Create tables and admin user
        with app.app_context():
            try:
                print("Creating all tables...")
                db.create_all()
                print("✅ Tables created successfully!")
                
                print("Checking for admin user...")
                admin = User.query.filter_by(username='admin').first()
                if not admin:
                    print("Creating admin user...")
                    admin = User(
                        username='admin',
                        password_hash=generate_password_hash('admin'),
                        is_admin=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("✅ Admin user created successfully!")
                else:
                    print("✅ Admin user already exists")
                
                # Verify key tables exist
                print("Verifying Block table...")
                block_count = Block.query.count()
                print(f"✅ Block table exists with {block_count} records")
                
                return True
                
            except SQLAlchemyError as e:
                print(f"SQLAlchemy error: {e}")
                return False
                
            except Exception as e:
                print(f"Unexpected error: {e}")
                return False
    
    except Exception as e:
        print(f"Global error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n✅ Direct database initialization completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Direct database initialization failed!")
        sys.exit(1)
