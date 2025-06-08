"""
Test script to verify the ImageStorage functionality
"""

def test_image_storage():
    """Test the ImageStorage backup and retrieval"""
    from app import create_app
    from app.models import db, ImageStorage
    import os
    import random
    
    app = create_app()
      # List of test images
    test_images = []
    basedir = os.path.abspath(os.path.dirname(__file__))
    uploads_dir = os.path.join(basedir, 'static', 'uploads')
    
    # Generate a list of existing images
    for filename in os.listdir(uploads_dir):
        if os.path.isfile(os.path.join(uploads_dir, filename)) and filename != '.gitkeep':
            test_images.append(filename)
    
    if not test_images:
        print("No test images found! Please upload some images first.")
        return
        
    with app.app_context():
        # Check database backup
        total = len(test_images)
        backed_up = 0
        
        for filename in test_images:
            img_storage = ImageStorage.query.filter_by(filename=filename).first()
            if img_storage and img_storage.binary_data:
                backed_up += 1
                print(f"✅ Image '{filename}' is backed up in database ({len(img_storage.binary_data)} bytes)")
            else:
                print(f"❌ Image '{filename}' is NOT backed up in database")
                
        print(f"\nSummary: {backed_up}/{total} images are backed up in the database")
        
        # Test restoration
        if backed_up > 0 and test_images:
            # Select a random image
            test_filename = random.choice(test_images)
            img_storage = ImageStorage.query.filter_by(filename=test_filename).first()
            
            if img_storage and img_storage.binary_data:                # Create a temp restore directory
                restore_dir = os.path.join(basedir, 'static', 'restored')
                os.makedirs(restore_dir, exist_ok=True)
                
                # Write the file
                restore_path = os.path.join(restore_dir, test_filename)
                with open(restore_path, 'wb') as f:
                    f.write(img_storage.binary_data)
                
                print(f"\nTest Restore: Successfully restored '{test_filename}' to {restore_path}")
                print(f"Original size: {os.path.getsize(os.path.join(uploads_dir, test_filename))} bytes")
                print(f"Restored size: {os.path.getsize(restore_path)} bytes")
                
                # Clean up
                os.remove(restore_path)
                
if __name__ == '__main__':
    test_image_storage()
