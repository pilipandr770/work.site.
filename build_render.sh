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

# Emergency fix for Cyrillic table - run this first!
echo "EMERGENCY: Creating Cyrillic table directly..."
python emergency_cyrillic_table.py

# Patch model table names
echo "Patching model table names for correct mapping..."
python patch_model_tablenames.py

# Apply the direct model patch
echo "Applying direct model patch for Cyrillic table name..."
python patch_models_file.py

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

# Try Cyrillic table creation as backup
echo "Attempting Cyrillic table creation as backup..."
python create_cyrillic_block.py

# Verify database tables exist
echo "Final verification of database tables..."
python check_database_tables.py

echo "=== BUILD PROCESS COMPLETED ==="
