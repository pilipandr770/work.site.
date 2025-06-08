#!/bin/bash
# build_render.sh - Run during the build phase on Render.com

echo "=== STARTING BUILD PROCESS ==="

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Make scripts executable
echo "Making scripts executable..."
chmod +x prestart.sh
chmod +x *.py

# ABSOLUTELY FINAL FIX: Create both tables with sync triggers
echo "FINAL FIX: Creating both Cyrillic and Latin tables with sync triggers..."
python final_dual_tables_fix.py

# Apply SQLAlchemy monkey patch for table names
echo "Applying SQLAlchemy table name patch..."
python sqlalchemy_table_patch.py

# Apply flexible table name solution
echo "Applying flexible table name solution..."
python flexible_block_tablename.py

# DEFINITIVE FIX for Cyrillic block table issue as backup
echo "APPLYING DEFINITIVE CYRILLIC BLOCK TABLE FIX..."
python fix_cyrillic_block_table_definitive.py

# Only run these if all previous fixes fail
if [ $? -ne 0 ]; then
    echo "⚠️ All advanced fixes failed, trying emergency methods..."
    
    # Emergency fix for Cyrillic table
    echo "Creating Cyrillic table directly..."
    python emergency_cyrillic_table.py
    
    # Fix Block model with explicit Cyrillic name
    echo "Fixing Block model with explicit Cyrillic name..."
    python fix_block_model.py
    
    # Initialize database tables using robust method
    echo "Initializing database tables using robust strategy..."
    python robust_db_init.py
    
    # Specifically fix the block table issue
    echo "Fixing block table issue..."
    python fix_block_table.py
    
    # Check ORM model mapping
    echo "Checking ORM model mapping..."
    python check_orm_mapping.py
fi

# Final verification
echo "Final verification of database tables..."
python check_database_tables.py

echo "=== BUILD PROCESS COMPLETED ==="
