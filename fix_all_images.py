"""
Script to fix missing product and blog images.
This script will copy missing images from any available backup to the correct locations.
"""

import os
import shutil
from app import create_app, db
from app.models import BlogPost, Product
import glob

def fix_missing_images():
    """Fix missing images by copying from backup locations."""
    app = create_app()
    with app.app_context():
        # Define directories
        static_dir = os.path.join(app.root_path, 'static')
        uploads_dir = os.path.join(static_dir, 'uploads')
        blog_uploads_dir = os.path.join(uploads_dir, 'blog')
        
        # Ensure directories exist
        os.makedirs(uploads_dir, exist_ok=True)
        os.makedirs(blog_uploads_dir, exist_ok=True)
        
        # Define potential backup locations
        backup_locations = [
            os.path.join(app.root_path, '..', 'uploads_backup_20250608_162207'),
            os.path.join(app.root_path, '..', 'uploads'),
        ]
        
        # Scan for actual available backup dirs
        available_backups = []
        for location in backup_locations:
            if os.path.exists(location) and os.path.isdir(location):
                available_backups.append(location)
                print(f"Found backup directory: {location}")
        
        if not available_backups:
            print("No backup directories found!")
            return
        
        # Get product images to fix
        products = Product.query.filter(Product.image.isnot(None)).all()
        print(f"\nFound {len(products)} products with image references")
        
        # Process product images
        fixed_product_images = 0
        missing_product_images = 0
        
        for product in products:
            image_name = product.image
            if not image_name:
                continue
            
            # Skip if image already exists
            target_path = os.path.join(uploads_dir, image_name)
            if os.path.exists(target_path):
                print(f"✅ Product image already exists: {image_name}")
                continue
            
            # Try to find and copy image from backups
            found = False
            for backup_dir in available_backups:
                source_path = os.path.join(backup_dir, image_name)
                if os.path.exists(source_path):
                    shutil.copy2(source_path, target_path)
                    print(f"✅ Restored product image from backup: {image_name}")
                    fixed_product_images += 1
                    found = True
                    break
            
            if not found:
                print(f"❌ Could not find product image: {image_name} for product: {product.name}")
                missing_product_images += 1
        
        # Get blog posts to fix
        blog_posts = BlogPost.query.filter(BlogPost.featured_image.isnot(None)).all()
        print(f"\nFound {len(blog_posts)} blog posts with image references")
        
        # Process blog images
        fixed_blog_images = 0
        missing_blog_images = 0
        
        for post in blog_posts:
            image_name = post.featured_image
            if not image_name:
                continue
            
            # Clean filename (remove path prefix if present)
            clean_name = image_name.replace('blog/', '') if image_name.startswith('blog/') else image_name
            
            # Update the database if needed
            if image_name != clean_name:
                post.featured_image = clean_name
                db.session.add(post)
                print(f"📄 Updated database entry for blog post: {post.title}: {image_name} -> {clean_name}")
            
            # Skip if image already exists in blog uploads
            blog_target_path = os.path.join(blog_uploads_dir, clean_name)
            if os.path.exists(blog_target_path):
                print(f"✅ Blog image already exists in blog dir: {clean_name}")
                continue
            
            # Skip if image already exists in main uploads
            main_target_path = os.path.join(uploads_dir, clean_name)
            if os.path.exists(main_target_path):
                # Copy from main uploads to blog uploads
                shutil.copy2(main_target_path, blog_target_path)
                print(f"✅ Copied blog image from main uploads: {clean_name}")
                fixed_blog_images += 1
                continue
            
            # Try to find and copy image from backups
            found = False
            for backup_dir in available_backups:
                source_path = os.path.join(backup_dir, clean_name)
                if os.path.exists(source_path):
                    # Copy to both main uploads and blog uploads
                    shutil.copy2(source_path, main_target_path)
                    shutil.copy2(source_path, blog_target_path)
                    print(f"✅ Restored blog image from backup: {clean_name}")
                    fixed_blog_images += 1
                    found = True
                    break
            
            if not found:
                print(f"❌ Could not find blog image: {clean_name} for post: {post.title}")
                missing_blog_images += 1
        
        # Commit any database changes
        db.session.commit()
        
        # Print summary
        print("\n--- SUMMARY ---")
        print(f"Total products with images: {len(products)}")
        print(f"Product images fixed: {fixed_product_images}")
        print(f"Product images still missing: {missing_product_images}")
        print(f"Total blog posts with images: {len(blog_posts)}")
        print(f"Blog images fixed: {fixed_blog_images}")
        print(f"Blog images still missing: {missing_blog_images}")
        
if __name__ == "__main__":
    fix_missing_images()
