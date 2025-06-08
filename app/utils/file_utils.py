"""
Utility functions for file operations
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def save_uploaded_file(file, folder='uploads', use_uuid=True):
    """
    Saves an uploaded file to the specified folder with proper path handling
    
    Args:
        file: The FileStorage object from form.field.data
        folder: Subfolder in static to save to (default: 'uploads')
        use_uuid: Whether to use UUID for filename (default: True)
        
    Returns:
        The saved filename (not the full path)
    """
    if not file or not hasattr(file, 'filename') or not file.filename:
        return None
        
    if use_uuid:
        # Generate unique filename with UUID
        extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        filename = f"{str(uuid.uuid4())}.{extension}"
    else:
        # Use secure version of original filename
        filename = secure_filename(file.filename)
    
    # Get the absolute path to the project root
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    upload_folder = os.path.join(basedir, 'app', 'static', folder)
    
    # Ensure the folder exists
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_folder, filename)
    file.save(file_path)
    
    # Return only the filename, not the full path
    return filename
