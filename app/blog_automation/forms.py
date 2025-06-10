"""
Forms for blog automation
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (StringField, TextAreaField, BooleanField, SelectField,
                    SubmitField, TimeField, SelectMultipleField, widgets)
from wtforms.validators import DataRequired, Optional, Length

class MultiCheckboxField(SelectMultipleField):
    """Custom field for multiple checkbox selection"""
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class BlogTopicForm(FlaskForm):
    """Form for adding/editing blog topics"""
    title = StringField('Topic Title', validators=[DataRequired(), Length(max=255)])
    description = TextAreaField('Description/Keywords', validators=[Optional()])
    scheduled_for = TimeField('Schedule For (optional)', format='%H:%M', validators=[Optional()])
    submit = SubmitField('Save')

class TopicBulkUploadForm(FlaskForm):
    """Form for bulk uploading blog topics"""
    file = FileField('CSV File', validators=[
        DataRequired(),
        FileAllowed(['csv'], 'CSV files only!')
    ])
    submit = SubmitField('Upload')

class AutopostingSettingsForm(FlaskForm):
    """Form for configuring autoposting settings"""
    is_active = BooleanField('Enable Automated Posting')
    
    # Days of week as checkboxes
    days_of_week = MultiCheckboxField('Days of Week', 
        choices=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday')
        ]
    )
    
    posting_time = TimeField('Posting Time', format='%H:%M', validators=[DataRequired()])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Handle string to time conversion for database values
        if hasattr(self, 'posting_time') and isinstance(self.posting_time.data, str):
            try:
                # Convert string HH:MM to time object
                from datetime import datetime, time
                time_parts = self.posting_time.data.split(':')
                if len(time_parts) == 2:
                    hour = int(time_parts[0])
                    minute = int(time_parts[1])
                    self.posting_time.data = time(hour=hour, minute=minute)
            except (ValueError, IndexError):
                # If conversion fails, set to default time
                self.posting_time.data = None
    # Translation settings
    auto_translate = BooleanField('Automatically Translate Content')
    target_languages = MultiCheckboxField('Target Languages', 
        choices=[
            ('en', 'English'),
            ('de', 'German'),
            ('ru', 'Russian')
        ]
    )
    
    # Image generation
    generate_images = BooleanField('Generate Images for Posts')
    image_style = StringField('Image Style Description', validators=[Optional()])
    
    # Social media
    post_to_telegram = BooleanField('Post to Telegram')
    
    submit = SubmitField('Save Settings')
