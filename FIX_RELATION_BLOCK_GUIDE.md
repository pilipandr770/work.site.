# Fix for "relation 'block' does not exist" Error

## Problem

Your application is encountering the following error:

```
sqlalchemy.exc.ProgrammingError: (psycopg2.errors.UndefinedTable) relation "block" does not exist
```

This happens because the PostgreSQL database doesn't have the required tables, specifically the 'block' table.

## Automated Solutions

We've added multiple automated solutions that should fix this issue during deployment:

1. `robust_db_init.py` - A multi-strategy script that tries different approaches to create tables
2. `fix_block_table.py` - A specialized script that focuses on fixing the block table issue
3. Enhanced `direct_init_db.py` and `direct_sql_init.py` scripts

## Manual Fix

If you still encounter this issue, here's how to fix it manually through the Render shell:

1. Access the Render shell in the dashboard
2. Run the specialized fix script:
   ```
   python fix_block_table.py
   ```

3. If that doesn't work, try the direct SQL method:
   ```
   python direct_sql_init.py
   ```

4. Verify the tables exist:
   ```
   python check_database_tables.py
   ```

## PostgreSQL Commands

If you need to check or fix the issue directly with PostgreSQL commands:

1. Connect to the PostgreSQL database using the connection string from the Render environment variables:
   ```
   psql $DATABASE_URL
   ```

2. Check which tables exist:
   ```sql
   \dt
   ```

3. Create the block table manually:
   ```sql
   CREATE TABLE block (
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

4. Verify the block table is created:
   ```sql
   SELECT COUNT(*) FROM block;
   ```

## Note About Case Sensitivity

PostgreSQL treats unquoted table names as lowercase. If your model defines the table as "Block" but the actual table name should be "block", this might cause issues. Our fix scripts ensure the correct case is used.

## After Fixing

After applying the fix, restart your service in the Render dashboard for the changes to take effect. The application should now work without the "relation 'block' does not exist" error.
