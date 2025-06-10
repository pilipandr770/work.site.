import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models import BlogPost
from sqlalchemy import desc, func
from datetime import datetime
import json

def debug_blog_posts():
    """Debug function to check blog posts in the database"""
    app = create_app()
    with app.app_context():
        print('=== DEBUG: BLOG POSTS IN DATABASE ===')
        all_posts = BlogPost.query.all()
        
        print(f'Total posts: {len(all_posts)}')
        for post in all_posts:
            print(f'ID: {post.id}')
            print(f'Title: {post.title}')
            print(f'Slug: {post.slug}')
            print(f'Is Published: {post.is_published}')
            print(f'Publish Date: {post.publish_date}')
            print(f'Created At: {post.created_at}')
            print('---')
        
        print('\n=== DEBUG: PUBLISHED POSTS QUERY ===')
        now = datetime.utcnow()
        published_posts = BlogPost.query.filter(
            BlogPost.is_published == True,
            (BlogPost.publish_date <= now) | (BlogPost.publish_date == None)
        ).order_by(desc(func.coalesce(BlogPost.publish_date, BlogPost.created_at))).all()
        
        print(f'Published posts count: {len(published_posts)}')
        for i, post in enumerate(published_posts, 1):
            effective_date = post.publish_date if post.publish_date else post.created_at
            print(f'{i}. {post.title} (effective date: {effective_date})')

if __name__ == '__main__':
    debug_blog_posts()
