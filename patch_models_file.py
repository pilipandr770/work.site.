#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Runtime Model Patch
This script creates a patched version of the models.py file with the correct table name.
"""

import os
import sys
import shutil
from pathlib import Path

def patch_models_file():
    """Create a patched version of the models.py file."""
    print("=== PATCHING MODELS.PY FILE ===")
    
    # Define file paths
    models_file = Path("app/models.py")
    backup_file = Path("app/models.py.bak")
    
    if not models_file.exists():
        print(f"❌ Models file {models_file} not found!")
        return False
    
    # Make a backup of the original file
    print(f"Creating backup of {models_file} to {backup_file}")
    shutil.copy2(models_file, backup_file)
    
    # Read the original file
    try:
        with open(models_file, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        print(f"❌ Error reading models file: {e}")
        return False
    
    # Find the Block class definition
    block_class_idx = content.find("class Block(db.Model):")
    if block_class_idx == -1:
        print("❌ Could not find Block class definition in models.py!")
        return False
    
    # Insert __tablename__ attribute after the class definition
    class_def_end = content.find(":", block_class_idx) + 1
    modified_content = (
        content[:class_def_end] + 
        '\n    __tablename__ = "блок"  # Explicit Cyrillic table name' +
        content[class_def_end:]
    )
    
    # Write the modified file
    try:
        with open(models_file, 'w', encoding='utf-8') as file:
            file.write(modified_content)
        print(f"✅ Successfully patched {models_file} with explicit Cyrillic table name!")
        return True
    except Exception as e:
        print(f"❌ Error writing patched models file: {e}")
        # Restore from backup
        shutil.copy2(backup_file, models_file)
        print(f"Restored original file from backup {backup_file}")
        return False

def verify_patch():
    """Verify the patched models file works correctly."""
    print("\n=== VERIFYING MODEL PATCH ===")
    
    try:
        # Import the patched model
        from app import create_app, db
        from importlib import reload
        import app.models
        reload(app.models)  # Reload to get the patched version
        from app.models import Block
        
        # Check the table name
        tablename = getattr(Block, '__tablename__', 'unknown')
        print(f"Block.__tablename__ = {tablename}")
        
        if tablename == 'блок':
            print("✅ Block model now has correct Cyrillic table name!")
            return True
        else:
            print(f"❌ Block model still has incorrect table name: {tablename}")
            return False
            
    except Exception as e:
        print(f"❌ Error verifying model patch: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("RUNTIME MODEL PATCH")
    print("This script patches the models.py file to use the correct table name")
    print("=" * 60)
    
    success = patch_models_file()
    
    if success:
        # Verify the patch worked
        verify_success = verify_patch()
        
        if verify_success:
            print("\n✅ Model patch completed and verified successfully!")
            sys.exit(0)
        else:
            print("\n⚠️ Model patch applied but verification failed!")
            sys.exit(1)
    else:
        print("\n❌ Model patch failed!")
        sys.exit(1)
