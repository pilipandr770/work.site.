# Fixing Cyrillic vs. Latin Table Name Issue

## Problem

You're encountering the following error:
```
psycopg2.errors.UndefinedTable: отношение "блок" не существует
СТРОКА 2: ИЗ блока  
```

This is a character encoding/naming issue. The application is looking for a table named `блок` (in Cyrillic) but the database has a table named `block` (in Latin alphabet), or vice versa.

## Solutions Implemented

We've implemented multiple solutions to fix this issue:

1. **Creating a view**: A SQL view named `блок` that references the `block` table
2. **Creating both tables**: Both a `block` table and a `блок` table with the same structure
3. **ORM mapping check**: A script that checks and fixes the mapping between the model and database
4. **Direct Cyrillic table creation**: A script that creates the Cyrillic table directly

## How to Fix Manually

If you're still experiencing this issue, follow these steps:

1. Connect to the Render shell
2. Run each of these scripts in sequence:

```bash
# First, try creating the block table with both Latin and Cyrillic names
python fix_block_table.py

# Then check the ORM mapping
python check_orm_mapping.py

# If that doesn't work, try direct Cyrillic table creation
python create_cyrillic_block.py
```

3. If the scripts run successfully but you still see the error, restart the service

## PostgreSQL Commands

If you need to fix this directly with PostgreSQL:

1. Connect to the database:
```
psql $DATABASE_URL
```

2. Check if the 'block' table exists:
```sql
\dt block
```

3. Create a view from 'block' to 'блок':
```sql
CREATE OR REPLACE VIEW "блок" AS SELECT * FROM block;
```

4. Or create a Cyrillic table directly:
```sql
CREATE TABLE "блок" (
    id SERIAL PRIMARY KEY,
    title VARCHAR(128),
    content TEXT,
    image VARCHAR(256),
    "order" INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT TRUE,
    slug VARCHAR(64) UNIQUE,
    is_top BOOLEAN DEFAULT FALSE,
    title_ua VARCHAR(128),
    title_en VARCHAR(128),
    title_de VARCHAR(128),
    title_ru VARCHAR(128),
    content_ua TEXT,
    content_en TEXT,
    content_ru TEXT,
    content_de TEXT
);
```

5. Verify the view or table was created:
```sql
\dv блок
\dt блок
```

## Long-term Fix

To fix this issue permanently, you should review your models.py file and ensure the table name is correctly specified:

```python
class Block(db.Model):
    __tablename__ = "block"  # Ensure this matches the actual table name in the database
    # rest of model definition...
```

This will ensure that the ORM is looking for the right table name in the database.
