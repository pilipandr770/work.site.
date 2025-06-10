# app/blog/routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, g, session
from flask_login import current_user
from app.models import db, BlogBlock
from app.forms import BlogBlockForm
from app.utils.file_utils import save_uploaded_file
from app.admin.routes import admin_required
import os
from datetime import datetime

from app.blog import blog_bp

# Вспомогательные функции для получения локализованного контента блога
def get_blog_block_title(block):
    """Получает заголовок блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.title  # Основной язык
    elif lang == 'en' and block.title_en:
        return block.title_en
    elif lang == 'de' and block.title_de:
        return block.title_de
    elif lang == 'ru' and block.title_ru:
        return block.title_ru
    return block.title

def get_blog_block_content(block):
    """Получает содержимое блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.content  # Основной язык
    elif lang == 'en' and block.content_en:
        return block.content_en
    elif lang == 'de' and block.content_de:
        return block.content_de
    elif lang == 'ru' and block.content_ru:
        return block.content_ru
    return block.content

def get_blog_block_summary(block):
    """Получает краткое описание блока блога в текущем языке"""
    lang = g.get('lang', session.get('lang', 'uk'))
    if lang == 'uk':
        return block.summary  # Основной язык
    elif lang == 'en' and block.summary_en:
        return block.summary_en
    elif lang == 'de' and block.summary_de:
        return block.summary_de
    elif lang == 'ru' and block.summary_ru:
        return block.summary_ru
    return block.summary

# Public blog routes
@blog_bp.route('/')
def index():
    """Main blog index page with all active blocks"""
    blocks = BlogBlock.query.filter_by(is_active=True).order_by(BlogBlock.position).all()
    
    return render_template('blog/index.html', 
                          blocks=blocks,
                          get_blog_block_title=get_blog_block_title,
                          get_blog_block_summary=get_blog_block_summary,
                          get_blog_block_content=get_blog_block_content)

@blog_bp.route('/<int:position>')
def block_detail(position):
    """Detail page for a specific block"""
    block = BlogBlock.query.filter_by(position=position, is_active=True).first_or_404()
    
    return render_template('blog/block_detail.html', 
                          block=block,
                          get_blog_block_title=get_blog_block_title,
                          get_blog_block_summary=get_blog_block_summary,
                          get_blog_block_content=get_blog_block_content)

# Admin routes for blog management
@blog_bp.route('/admin', strict_slashes=False)
@admin_required
def admin_dashboard():
    """Admin dashboard for the blog blocks"""
    blocks = []
    
    # Ensure we have all 12 blocks
    for position in range(1, 13):
        block = BlogBlock.query.filter_by(position=position).first()
        if not block:
            block = BlogBlock(
                title=f"Блок #{position}",
                content=f"Содержимое блока #{position}",
                summary=f"Краткое описание блока #{position}",
                position=position
            )
            db.session.add(block)
            db.session.commit()
        blocks.append(block)
    
    return render_template('blog/admin/dashboard.html', blocks=blocks)

@blog_bp.route('/admin/blocks/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_block(id):
    """Admin view for editing a blog block"""
    block = BlogBlock.query.get_or_404(id)
    form = BlogBlockForm(obj=block)
    
    if form.validate_on_submit():
        block.title = form.title.data
        block.title_en = form.title_en.data
        block.title_de = form.title_de.data
        block.title_ru = form.title_ru.data
        block.content = form.content.data
        block.content_en = form.content_en.data
        block.content_de = form.content_de.data
        block.content_ru = form.content_ru.data
        block.summary = form.summary.data
        block.summary_en = form.summary_en.data
        block.summary_de = form.summary_de.data
        block.summary_ru = form.summary_ru.data
        block.is_active = form.is_active.data
        
        # Handle featured image
        if form.featured_image.data:
            filename = save_uploaded_file(form.featured_image.data, 'uploads/blog')
            # Store just the filename without the path prefix
            if '/' in filename:
                block.featured_image = filename.split('/')[-1]
            else:
                block.featured_image = filename
        
        db.session.commit()
        flash('Блок успешно обновлен!', 'success')
        return redirect(url_for('blog.admin_dashboard'))
    
    return render_template('blog/admin/edit_block.html', form=form, block=block)
