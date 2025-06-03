# PowerShell script to commit and push database fix changes

# Show what's being committed
Write-Host "=== Files being committed ===" -ForegroundColor Cyan
git status

# Add the modified files
Write-Host "`n=== Adding modified files ===" -ForegroundColor Cyan
git add app/__init__.py
git add app/models.py
git add DB_CREATE_ALL_SOLUTION.md
git add FINAL_DATABASE_SOLUTION.md
git add CLEAN_DATABASE_FIX.md
git add verify_database_solution.py
git add reset_block_tablename.py
git add test_app_creation.py
git add test_db_tables_creation.py

# Commit the changes
Write-Host "`n=== Committing changes ===" -ForegroundColor Cyan
git commit -m "Fix 'relation block does not exist' error by adding db.create_all() and explicit tablename"

# Push to remote repository
Write-Host "`n=== Pushing changes ===" -ForegroundColor Cyan
git push

Write-Host "`n=== All done! Changes have been pushed to the repository ===" -ForegroundColor Green
Write-Host "The fix should be automatically deployed on Render.com" -ForegroundColor Green
