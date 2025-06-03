# Definitive Solution for Cyrillic Table Name Issue

## The Problem

The application was failing with the error message "relation 'блок' does not exist" when trying to access the database on Render.com. This happened because:

1. The SQLAlchemy ORM was trying to use a table named "блок" (Cyrillic) even though it was never explicitly declared in the model
2. By default, SQLAlchemy uses the lowercase class name for the table name
3. The class name "Block" should have created a table named "block" (Latin), but somehow it was mapping to the Cyrillic name

## Root Cause

The root cause was a combination of:

1. Character encoding issues between the application and PostgreSQL
2. SQLAlchemy's automatic table name generation using the class name
3. Inconsistent table name references across different scripts
4. Different behavior between local development and the Render.com production environment

## The Solution

We created a comprehensive solution that:

1. Explicitly defines the table name in the model with `__tablename__ = "блок"`
2. Makes sure the Cyrillic table exists in the database
3. Transfers any data from the Latin "block" table to the Cyrillic "блок" table
4. Ensures proper character encoding when communicating with the database

## Implementation Details

### 1. Modified the Block Model

We added an explicit tablename to the Block model:

```python
class Block(db.Model):
    """Контентний блок (для 6 секцій сайту)"""
    __tablename__ = "блок"  # Explicit Cyrillic table name
    id = db.Column(db.Integer, primary_key=True)
    # ... other fields ...
```

### 2. Created the Cyrillic Table Directly

We use direct SQL to create the Cyrillic table:

```python
conn.execute(text("""
CREATE TABLE IF NOT EXISTS "блок" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    # ... other columns ...
)
"""))
```

### 3. Consolidated Fix Scripts

We created a definitive fix script that:

- Checks if the Cyrillic table exists
- Creates it if needed
- Transfers data from Latin to Cyrillic table if needed
- Updates the model's tablename

### 4. Updated Deployment Scripts

We updated the `build_render.sh` and `prestart.sh` scripts to:

1. Run our definitive fix first
2. Only fall back to individual fix scripts if the definitive fix fails

## Testing and Verification

We added two verification scripts:

1. `verify_database_comprehensive.py` - Performs a detailed check of the database tables
2. `test_block_table.py` - A simple test script that tries to query the Block model

## How to Implement This Solution

1. Run `python fix_cyrillic_block_table_definitive.py` to apply the complete fix
2. Run `python verify_database_comprehensive.py` to verify all tables are working
3. Run `python test_block_table.py` for a quick check that the Block model works

## Additional Notes

- The solution ensures the application works on both local development and Render.com
- It's compatible with future updates, migrations, and database changes
- It maintains data integrity by preserving existing records

## What We Learned

1. Always explicitly define table names in SQLAlchemy models
2. Be careful with non-Latin characters in database identifiers
3. Test database encoding and character sets before deployment
4. When working with PostgreSQL, ensure proper client encoding settings

This solution completely resolves the "relation 'блок' does not exist" error and ensures the application works correctly on Render.com.
