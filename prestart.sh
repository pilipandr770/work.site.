#!/bin/bash
# prestart.sh - Runs before app startup on Render

echo "=== PRESTART CHECK ==="

# Test that db.create_all() is working in app/__init__.py
echo "Testing database table creation through db.create_all()..."
python test_db_tables_creation.py

# Only run these fixes if the db.create_all() approach fails
if [ $? -ne 0 ]; then
    echo "⚠️ db.create_all() didn't create all needed tables, applying alternative fixes..."
    
    # Create both tables with sync triggers
    echo "FINAL FIX: Creating both Cyrillic and Latin tables with sync triggers..."
    python final_dual_tables_fix.py
    
    # Apply SQLAlchemy monkey patch for table names
    echo "Applying SQLAlchemy table name patch..."
    python sqlalchemy_table_patch.py
    
    # Apply flexible table name solution
    echo "Applying flexible table name solution..."
    python flexible_block_tablename.py
fi

# DEFINITIVE FIX for Cyrillic block table issue as backup
echo "APPLYING DEFINITIVE CYRILLIC BLOCK TABLE FIX..."
python fix_cyrillic_block_table_definitive.py

# Create admin user if doesn't exist
echo "Checking for admin user and creating if needed..."
python create_admin_render.py

# Only run these if all previous fixes fail
if [ $? -ne 0 ]; then
    echo "⚠️ All advanced fixes failed, trying emergency methods..."
    
    # Emergency fix for Cyrillic table
    echo "Creating Cyrillic table directly..."
    python emergency_cyrillic_table.py
    
    # Apply direct model patch to fix Cyrillic table name
    echo "Applying direct model patch for Cyrillic table name..."
    python patch_models_file.py
    
    # Apply direct Block model fix 
    echo "Fixing Block model with explicit Cyrillic table name..."
    python fix_block_model.py
fi

# Environment diagnostics
echo "Checking environment variables..."
if [ -z "$DATABASE_URL" ]; then
    echo "WARNING: DATABASE_URL is not set!"
else
    echo "DATABASE_URL is set."
    
    # Check if URL contains localhost
    if [[ "$DATABASE_URL" == *"localhost"* ]] || [[ "$DATABASE_URL" == *"127.0.0.1"* ]]; then
        echo "ERROR: DATABASE_URL contains localhost, which won't work on Render!"
    fi
fi

# Check for installed packages
echo "Checking required packages..."
pip list | grep psycopg2

# Try to run migrations
echo "Running database migrations..."
echo "Current directory: $(pwd)"
echo "Python module path: $PYTHONPATH"
echo "Files in app directory:"
ls -la ./app/

# Try primary migrations method first
echo "Running migrations with app.migrations_update"
python -m app.migrations_update
if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully!"
else
    echo "⚠️ Standard migrations failed, trying robust initialization..."
    
    # Try the robust initialization script as fallback
    python robust_db_init.py
    if [ $? -eq 0 ]; then
        echo "✅ Robust database initialization completed successfully!"
    else
        echo "❌ All database initialization methods failed!"
        echo "The application may not work correctly. Check the logs above."
        
        # Run diagnostic script
        echo "Running database diagnostics..."
        python check_database_tables.py
        
        # Try direct table creation as last resort
        echo "Attempting direct table creation as last resort..."
        python direct_init_db.py
        
        # No matter what, run the specialized block table fix
        echo "Running specialized block table fix..."
        python fix_block_table.py
        
        # Always check and fix ORM mapping
        echo "Checking ORM model mapping..."
        python check_orm_mapping.py
        
        # If table is still missing, try direct SQL method
        if [ $? -ne 0 ]; then
            echo "Attempting direct SQL table creation as absolute last resort..."
            python direct_sql_init.py
            
            # Run ORM mapping check again
            python check_orm_mapping.py
            
            # As an absolute last resort, try creating a Cyrillic table
            if [ $? -ne 0 ]; then
                echo "Attempting to create Cyrillic 'блок' table as absolute last resort..."
                python create_cyrillic_block.py
            fi
        fi
    fi
fi

# Verify database tables exist
echo "Final database verification..."
python << EOF
import os
import sys
from sqlalchemy import create_engine, text

try:
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        print("ERROR: No DATABASE_URL found")
        sys.exit(1)
    
    if db_url.startswith('postgres://'):
        db_url = db_url.replace('postgres://', 'postgresql://', 1)
    
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_database()"))
        print(f"Connected to database: {result.scalar()}")
        
        result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"))
        tables = [row[0] for row in result]
        print(f"Tables in database: {', '.join(tables)}")
        
        # Check critical tables
        critical_tables = ['block', 'user', 'product', 'category']
        missing = [t for t in critical_tables if t not in tables]
        
        if missing:
            print(f"⚠️ WARNING: Missing critical tables: {', '.join(missing)}")
        else:
            print("✅ All critical tables exist")
except Exception as e:
    print(f"Error during database check: {e}")
EOF

echo "=== PRESTART CHECK COMPLETED ==="
