"""
Routes for blog automation
"""
import csv
import io
import os
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.utils import secure_filename

from app.models import db
from app.admin.routes import admin_required
from app.blog_automation import blog_automation_bp
from app.blog_automation.models import BlogTopic, AutopostingSchedule, ContentGenerationLog
from app.blog_automation.forms import BlogTopicForm, TopicBulkUploadForm, AutopostingSettingsForm
from app.blog_automation.scheduler import get_scheduler

@blog_automation_bp.route('/')
@admin_required
def index():
    """Blog automation dashboard"""
    # Get statistics
    total_topics = BlogTopic.query.count()
    pending_topics = BlogTopic.query.filter_by(status='pending').count()
    completed_topics = BlogTopic.query.filter_by(status='completed').count()
    failed_topics = BlogTopic.query.filter_by(status='failed').count()
    
    # Get autoposting settings
    settings = AutopostingSchedule.query.first()
    if not settings:
        settings = AutopostingSchedule()
        db.session.add(settings)
        db.session.commit()
    
    # Get recent logs
    logs = ContentGenerationLog.query.order_by(ContentGenerationLog.created_at.desc()).limit(10).all()
    
    return render_template('blog_automation/index.html', 
                           total_topics=total_topics,
                           pending_topics=pending_topics, 
                           completed_topics=completed_topics,
                           failed_topics=failed_topics,
                           settings=settings,
                           logs=logs)

@blog_automation_bp.route('/topics')
@admin_required
def topics():
    """Manage blog topics"""
    topics = BlogTopic.query.order_by(BlogTopic.created_at.desc()).all()
    return render_template('blog_automation/topics.html', topics=topics)

@blog_automation_bp.route('/topics/add', methods=['GET', 'POST'])
@admin_required
def add_topic():
    """Add a new blog topic"""
    form = BlogTopicForm()
    
    if form.validate_on_submit():
        topic = BlogTopic(
            title=form.title.data,
            description=form.description.data,
            status='pending'
        )
        
        if form.scheduled_for.data:
            # Convert time field to datetime for scheduling
            scheduled_time = form.scheduled_for.data
            now = datetime.utcnow()
            topic.scheduled_for = datetime(
                now.year, now.month, now.day,
                scheduled_time.hour, scheduled_time.minute
            )
        
        db.session.add(topic)
        db.session.commit()
        
        flash('Blog topic added successfully!', 'success')
        return redirect(url_for('blog_automation.topics'))
    
    return render_template('blog_automation/add_topic.html', form=form)

@blog_automation_bp.route('/topics/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_topic(id):
    """Edit blog topic"""
    topic = BlogTopic.query.get_or_404(id)
    form = BlogTopicForm(obj=topic)
    
    if form.validate_on_submit():
        topic.title = form.title.data
        topic.description = form.description.data
        
        if form.scheduled_for.data:
            # Convert time field to datetime for scheduling
            scheduled_time = form.scheduled_for.data
            now = datetime.utcnow()
            topic.scheduled_for = datetime(
                now.year, now.month, now.day,
                scheduled_time.hour, scheduled_time.minute
            )
        
        db.session.commit()
        flash('Topic updated successfully!', 'success')
        return redirect(url_for('blog_automation.topics'))
        
    return render_template('blog_automation/edit_topic.html', form=form, topic=topic)

@blog_automation_bp.route('/topics/<int:id>/delete', methods=['POST'])
@admin_required
def delete_topic(id):
    """Delete blog topic"""
    topic = BlogTopic.query.get_or_404(id)
    
    # Don't delete if content has already been generated
    if topic.blog_block_id:
        flash('Cannot delete a topic that has already generated content!', 'danger')
        return redirect(url_for('blog_automation.topics'))
    
    db.session.delete(topic)
    db.session.commit()
    
    flash('Topic deleted successfully!', 'success')
    return redirect(url_for('blog_automation.topics'))

@blog_automation_bp.route('/topics/bulk-upload', methods=['GET', 'POST'])
@admin_required
def bulk_upload_topics():
    """Bulk upload blog topics from CSV"""
    form = TopicBulkUploadForm()
    
    if form.validate_on_submit():
        csv_file = request.files['file']
        
        if csv_file:
            csv_data = csv_file.read().decode('utf-8')
            reader = csv.reader(io.StringIO(csv_data))
            
            # Skip header row if it exists
            header = next(reader, None)
            
            count = 0
            for row in reader:
                if row and len(row) >= 1:
                    title = row[0].strip()
                    description = row[1].strip() if len(row) > 1 else ""
                    
                    # Skip empty rows
                    if not title:
                        continue
                    
                    topic = BlogTopic(
                        title=title,
                        description=description,
                        status='pending'
                    )
                    
                    db.session.add(topic)
                    count += 1
            
            db.session.commit()
            flash(f'Successfully imported {count} topics!', 'success')
            return redirect(url_for('blog_automation.topics'))
    
    return render_template('blog_automation/bulk_upload.html', form=form)

@blog_automation_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    """Manage autoposting settings"""
    # Get or create settings
    settings = AutopostingSchedule.query.first()
    if not settings:
        settings = AutopostingSchedule()
        db.session.add(settings)
        db.session.commit()
    
    # Create form and properly populate time field
    from datetime import datetime, time
    
    form_data = {}
    if request.method == 'GET':
        # Handle the posting_time conversion from string to time object
        if settings.posting_time:
            try:
                time_parts = settings.posting_time.split(':')
                if len(time_parts) == 2:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    form_data['posting_time'] = time(hour=hour, minute=minute)
            except (ValueError, IndexError):
                # If conversion fails, don't set the time
                pass
    
    # Create form with settings object and any manual overrides
    form = AutopostingSettingsForm(obj=settings, data=form_data)
    
    # Pre-populate days of week and languages
    if request.method == 'GET':
        form.days_of_week.data = settings.days_of_week.split(',')
        form.target_languages.data = settings.target_languages.split(',')
    
    if form.validate_on_submit():
        settings.is_active = form.is_active.data
        settings.days_of_week = ','.join(form.days_of_week.data)
        # Make sure posting_time is a TimeField object before calling strftime
        if form.posting_time.data and hasattr(form.posting_time.data, 'strftime'):
            settings.posting_time = form.posting_time.data.strftime('%H:%M')
        elif isinstance(form.posting_time.data, str):
            # If it's already a string, just use it directly
            settings.posting_time = form.posting_time.data
        settings.auto_translate = form.auto_translate.data
        settings.target_languages = ','.join(form.target_languages.data)
        settings.generate_images = form.generate_images.data
        settings.image_style = form.image_style.data
        settings.post_to_telegram = form.post_to_telegram.data
        
        db.session.commit()
        
        # If settings are active, ensure scheduler is running
        if settings.is_active:
            scheduler = get_scheduler(current_app)
            if scheduler:
                scheduler.start()
        
        flash('Settings saved successfully!', 'success')
        return redirect(url_for('blog_automation.settings'))
    
    return render_template('blog_automation/settings.html', form=form, settings=settings)

@blog_automation_bp.route('/logs')
@admin_required
def logs():
    """View content generation logs"""
    logs = ContentGenerationLog.query.order_by(ContentGenerationLog.created_at.desc()).limit(100).all()
    return render_template('blog_automation/logs.html', logs=logs)

@blog_automation_bp.route('/test-content-generation/<int:topic_id>', methods=['POST'])
@admin_required
def test_content_generation(topic_id):
    """Test content generation for a specific topic"""
    topic = BlogTopic.query.get_or_404(topic_id)
    
    # Get the scheduler
    scheduler = get_scheduler(current_app)
    if not scheduler:
        flash('Scheduler not available!', 'danger')
        return redirect(url_for('blog_automation.topics'))
    
    # Get settings
    settings = AutopostingSchedule.query.first()
    if not settings:
        settings = AutopostingSchedule()
        db.session.add(settings)
        db.session.commit()
    
    # Run the processing (normally done by scheduler)
    scheduler._process_topic(topic, settings)
    
    flash('Test generation complete! Check logs for details.', 'info')
    return redirect(url_for('blog_automation.logs'))
