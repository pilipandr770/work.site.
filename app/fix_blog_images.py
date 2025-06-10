"""
Script to fix blog images and ensure they are properly formatted and accessible.
This script:
1. Makes sure all blog post images are properly stored in app/static/uploads/blog/
2. Updates database entries to have correct image path formats
"""

import os
import shutil
from app import create_app, db
from app.models import BlogPost
from pathlib import Path

def main():
    app = create_app()
    with app.app_context():
        # Ensure blog uploads directory exists
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
        blog_uploads_dir = os.path.join(uploads_dir, 'blog')
        os.makedirs(blog_uploads_dir, exist_ok=True)
        print(f"✅ Ensuring blog uploads directory exists at: {blog_uploads_dir}")

        # Get all blog posts with featured images
        blog_posts = BlogPost.query.filter(BlogPost.featured_image.isnot(None)).all()
        print(f"Found {len(blog_posts)} blog posts with featured images")

        for post in blog_posts:
            if not post.featured_image:
                continue

            # Clean up the image path
            # Remove 'blog/' prefix if it exists
            clean_filename = post.featured_image.replace('blog/', '') if post.featured_image.startswith('blog/') else post.featured_image

            # Check if the file exists in any of the possible locations
            # First, check in uploads/blog directory
            blog_path = os.path.join(blog_uploads_dir, clean_filename)
            main_path = os.path.join(uploads_dir, clean_filename)
            backup_path = os.path.join(app.root_path, '..', 'uploads_backup_20250608_162207', clean_filename)
            
            # Try to find the image and copy it to the blog uploads directory
            if os.path.exists(blog_path):
                print(f"✅ Image already exists in blog directory: {clean_filename}")
            elif os.path.exists(main_path):
                print(f"🔄 Copying image from main uploads to blog directory: {clean_filename}")
                shutil.copy2(main_path, blog_path)
            elif os.path.exists(backup_path):
                print(f"🔄 Restoring image from backup: {clean_filename}")
                shutil.copy2(backup_path, blog_path)
            else:
                print(f"❌ Could not find image: {clean_filename}")
                continue
            
            # Update the database entry if needed
            if post.featured_image != clean_filename:
                print(f"🔄 Updating database entry for post: {post.title} - {post.featured_image} -> {clean_filename}")
                post.featured_image = clean_filename
                db.session.add(post)

        # Commit all changes
        db.session.commit()
        print("✅ All updates committed to the database")

if __name__ == "__main__":
    main()
