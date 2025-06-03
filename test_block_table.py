#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Quick Block Table Test
This script tries to query the Block model and reports success or failure.
Use it for a quick check if the Cyrillic table fix is working.
"""

import os
import sys

def test_block_query():
    """Test if we can query the Block model."""
    print("Testing Block model query...")
    
    try:
        from app import create_app, db
        from app.models import Block
        
        # Get table name
        tablename = getattr(Block, '__tablename__', None)
        print(f"Block.__tablename__ = {tablename}")
        
        # Create app context and test query
        app = create_app()
        with app.app_context():
            # Try to get all blocks
            blocks = Block.query.all()
            count = len(blocks)
            
            print(f"✅ SUCCESS! Block query returned {count} records")
            
            if count > 0:
                print("\nSample data:")
                for i, block in enumerate(blocks[:3]):  # Show up to 3 blocks
                    print(f"  Block #{i+1}: id={block.id}, title='{block.title}'")
            
            return True
    
    except Exception as e:
        print(f"❌ FAILED! Error querying Block model: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("QUICK BLOCK TABLE TEST")
    print("=" * 60)
    
    success = test_block_query()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ TEST PASSED: Block table is working correctly!")
        sys.exit(0)
    else:
        print("❌ TEST FAILED: Block table is still not working!")
        sys.exit(1)
