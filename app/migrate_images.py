"""
Database migration script to add ImageStorage table
"""
from app import db
from app.models import ImageStorage
import os
from app.utils.file_utils import save_uploaded_file

def create_image_storage_table():
    """Create the ImageStorage table if it doesn't exist"""
    # Check if table exists
    if not ImageStorage.__tablename__ in db.metadata.tables:
        db.create_all()
        print("ImageStorage table created successfully")
    else:
        print("ImageStorage table already exists")
    
def migrate_existing_images():
    """Migrate existing images in the filesystem to the database"""
    # Get absolute path to uploads folder
    basedir = os.path.abspath(os.path.dirname(__file__))  # app directory
    uploads_dir = os.path.join(basedir, 'static', 'uploads')
    
    # Check if folder exists
    if not os.path.isdir(uploads_dir):
        print(f"Uploads directory not found: {uploads_dir}")
        return
        
    # List all files in uploads directory
    files = [f for f in os.listdir(uploads_dir) if os.path.isfile(os.path.join(uploads_dir, f))]
    print(f"Found {len(files)} files in uploads directory")
    
    # Process each file
    migrated = 0
    for filename in files:
        # Skip .gitkeep files
        if filename == '.gitkeep':
            continue
            
        # Check if already in database
        existing = ImageStorage.query.filter_by(filename=filename).first()
        if existing:
            print(f"File already backed up: {filename}")
            continue
            
        # Open and store the file
        file_path = os.path.join(uploads_dir, filename)
        try:
            with open(file_path, 'rb') as f:
                # Determine content type based on extension
                content_type = None
                if '.' in filename:
                    ext = filename.rsplit('.', 1)[1].lower()
                    if ext in ['jpg', 'jpeg']:
                        content_type = 'image/jpeg'
                    elif ext == 'png':
                        content_type = 'image/png'
                    elif ext == 'gif':
                        content_type = 'image/gif'
                    elif ext in ['mp4', 'mpeg4']:
                        content_type = 'video/mp4'
                
                # Create ImageStorage record
                image_storage = ImageStorage(
                    filename=filename,
                    binary_data=f.read(),
                    content_type=content_type
                )
                db.session.add(image_storage)
                db.session.commit()
                migrated += 1
                print(f"Migrated: {filename}")
        except Exception as e:
            print(f"Error migrating file {filename}: {str(e)}")
    
    print(f"Migration complete. {migrated} files backed up to database.")

if __name__ == '__main__':
    # Use app factory function
    from app import create_app
    app = create_app()
    with app.app_context():
        create_image_storage_table()
        migrate_existing_images()
