#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility to restore missing images from the database backup
"""

def restore_missing_images():
    """
    Check all images referenced in the database and restore any missing files
    from the backup data in ImageStorage table
    """
    from app import create_app, db
    from app.models import ImageStorage, Block, Product, ProductImage, PaymentMethod, BlogPost
    
    app = create_app()
    import os
    
    # Track statistics
    stats = {
        'checked': 0,
        'missing': 0,
        'restored': 0,
        'failed': 0
    }
    
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploads_dir = os.path.join(basedir, 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Create blog images directory
    blog_dir = os.path.join(uploads_dir, 'blog')
    os.makedirs(blog_dir, exist_ok=True)
    
    # Helper function to check and restore image
    def check_and_restore_image(filename):
        if not filename:
            return
            
        stats['checked'] += 1
        filepath = os.path.join(uploads_dir, filename)
        
        if os.path.isfile(filepath):
            return  # File exists, no need to restore
            
        stats['missing'] += 1
        print(f"Missing file: {filename}")
        
        # Look for backup in database
        img_storage = ImageStorage.query.filter_by(filename=filename).first()
        if img_storage and img_storage.binary_data:
            try:
                # Ensure directory exists
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                
                with open(filepath, 'wb') as f:
                    f.write(img_storage.binary_data)
                stats['restored'] += 1
                print(f"✅ Restored: {filename}")
            except Exception as e:
                stats['failed'] += 1
                print(f"❌ Failed to restore {filename}: {str(e)}")
        else:
            stats['failed'] += 1
            print(f"❌ No backup found for: {filename}")
    
    # Also check backup folder
    def restore_from_backup_folder():
        backup_dir = os.path.join(os.path.dirname(basedir), 'uploads_backup_20250608_162207')
        if not os.path.exists(backup_dir):
            print(f"Backup directory not found: {backup_dir}")
            return
            
        print(f"Checking backup folder: {backup_dir}")
        
        for filename in os.listdir(backup_dir):
            if filename.startswith('.'):  # Skip hidden files
                continue
                
            src_path = os.path.join(backup_dir, filename)
            if os.path.isfile(src_path):
                dest_path = os.path.join(uploads_dir, filename)
                blog_dest_path = os.path.join(blog_dir, filename)
                
                # Check if the file is needed in any folder
                if not os.path.exists(dest_path):
                    try:
                        with open(src_path, 'rb') as src_file:
                            content = src_file.read()
                            
                        with open(dest_path, 'wb') as dest_file:
                            dest_file.write(content)
                            
                        print(f"✅ Copied from backup: {filename}")
                        stats['restored'] += 1
                    except Exception as e:
                        print(f"❌ Failed to copy {filename} from backup: {str(e)}")
                        stats['failed'] += 1
                
                # If it's an image, also copy to blog folder
                if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')) and not os.path.exists(blog_dest_path):
                    try:
                        with open(src_path, 'rb') as src_file:
                            content = src_file.read()
                            
                        with open(blog_dest_path, 'wb') as dest_file:
                            dest_file.write(content)
                            
                        print(f"✅ Copied to blog folder: {filename}")
                        stats['restored'] += 1
                    except Exception as e:
                        print(f"❌ Failed to copy {filename} to blog folder: {str(e)}")
                        stats['failed'] += 1
    
    with app.app_context():
        # Check Block images
        for block in Block.query.all():
            check_and_restore_image(block.image)
            
        # Check Product images
        for product in Product.query.all():
            check_and_restore_image(product.image)
            
        # Check ProductImage records
        for img in ProductImage.query.all():
            check_and_restore_image(img.image_path)
            
        # Check PaymentMethod QR codes
        for method in PaymentMethod.query.all():
            check_and_restore_image(method.qr_code)
            
        # Check BlogPost featured images
        for post in BlogPost.query.all():
            if post.featured_image:
                # Blog images are stored in uploads/blog/ subdirectory
                
                # If the path already includes 'blog/', use as is
                if post.featured_image.startswith('blog/'):
                    check_and_restore_image(post.featured_image)
                else:
                    # Otherwise, check both with and without blog/ prefix
                    check_and_restore_image(f"blog/{post.featured_image}")
                    check_and_restore_image(post.featured_image)
        
        # Also try to restore from backup folder
        restore_from_backup_folder()
            
    # Print summary
    print("\nRestore Summary:")
    print(f"Files checked: {stats['checked']}")
    print(f"Missing files: {stats['missing']}")
    print(f"Successfully restored: {stats['restored']}")
    print(f"Failed to restore: {stats['failed']}")
    
if __name__ == '__main__':
    restore_missing_images()
