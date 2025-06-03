# Fixing PostgreSQL 'relation "блок" does not exist' Error - Final Solution

## Problem Identified

After analyzing the error logs, we've identified a specific issue:

The error message shows that the application is looking for a table named `блок` (Cyrillic) but the database has a table named `block` (Latin alphabet). This is likely due to character encoding issues or model configuration.

## Comprehensive Solution

We've implemented a multi-stage solution to fix this issue:

1. **Character Encoding Fix**:
   - Setting explicit UTF-8 encoding for database connections
   - Checking and reporting server and client encodings

2. **Table Creation With Multiple Names**:
   - Creating the table with Latin name (`block`)
   - Creating a view or table with Cyrillic name (`блок`)
   - Creating aliases between the tables

3. **ORM Mapping Fix**:
   - Patching table names in models at runtime
   - Explicitly setting `__tablename__` attribute

4. **Multiple Fallback Mechanisms**:
   - Direct SQL creation if ORM fails
   - View creation if table exists but with wrong name
   - Complete table recreation as last resort

## Updated Files

1. **New Scripts**:
   - `fix_block_table.py`: Focused fix for the block table issue
   - `create_cyrillic_block.py`: Emergency creation of Cyrillic table
   - `check_orm_mapping.py`: Fixes ORM model mapping issues
   - `patch_model_tablenames.py`: Runtime patching of model table names

2. **Updated Scripts**:
   - `build_render.sh`: Added model patching and table fixes
   - `prestart.sh`: Added additional checks and fallback mechanisms

3. **New Documentation**:
   - `CYRILLIC_TABLE_NAME_FIX.md`: Guide for fixing Cyrillic table name issues

## Deployment Instructions

1. **Push Changes to Repository**:
   ```bash
   git add .
   git commit -m "Fix for 'relation block does not exist' with Cyrillic table name solution"
   git push
   ```

2. **Redeploy on Render.com**:
   - Go to your Render.com dashboard
   - Select your service
   - Click "Manual Deploy" > "Deploy latest commit"

3. **Monitor Build Logs**:
   - Watch for successful execution of:
     - `patch_model_tablenames.py`
     - `fix_block_table.py`
     - `check_orm_mapping.py`
     - `create_cyrillic_block.py`

4. **Verify Success**:
   - The application should start without the "relation does not exist" error
   - You should be able to access the homepage

5. **If Issues Persist**:
   - Connect to Render shell
   - Run diagnostic scripts:
     ```bash
     python check_database_tables.py
     python fix_block_table.py
     python create_cyrillic_block.py
     ```
   - Check logs for specific errors

## Long-term Fixes

For a permanent solution, consider:

1. **Update Models.py**: Explicitly set `__tablename__` for all models
   ```python
   class Block(db.Model):
       __tablename__ = "block"  # Explicitly set table name
       # ...rest of model...
   ```

2. **Database Migration**: Create proper database migrations for future changes
   ```bash
   # Using Flask-Migrate or Alembic
   flask db init
   flask db migrate
   flask db upgrade
   ```

3. **Character Encoding**: Ensure consistent UTF-8 encoding across your application
   ```python
   # In database connection code
   engine = create_engine(url, connect_args={"client_encoding": "utf8"})
   ```

This comprehensive solution addresses the specific issue while providing multiple fallback mechanisms to ensure your application works correctly on Render.com.
