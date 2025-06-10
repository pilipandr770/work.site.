"""
Script to create placeholder images for missing product images
"""

import os
from PIL import Image, ImageDraw, ImageFont
from app import create_app, db
from app.models import Product

def create_placeholder_image(text, save_path, width=400, height=300, bg_color=(230, 230, 230), text_color=(100, 100, 100)):
    """Create a placeholder image with text"""
    img = Image.new('RGB', (width, height), color=bg_color)
    d = ImageDraw.Draw(img)
    
    # Use a default font
    try:
        font = ImageFont.truetype("arial", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Wrap text if too long
    text_lines = []
    words = text.split()
    current_line = words[0]
    
    for word in words[1:]:
        test_line = current_line + " " + word
        # Approximate width calculation
        if len(test_line) * 10 < width:  # Simple estimation
            current_line = test_line
        else:
            text_lines.append(current_line)
            current_line = word
    
    text_lines.append(current_line)
    
    # Add product placeholder text
    text_lines.insert(0, "")
    text_lines.insert(0, "Product Placeholder")
    
    # Calculate total text height for centering
    line_height = 30
    total_height = len(text_lines) * line_height
    y_position = (height - total_height) // 2
    
    # Draw each line
    for line in text_lines:
        text_width = len(line) * 10  # Simple estimation
        x_position = (width - text_width) // 2
        d.text((x_position, y_position), line, fill=text_color, font=font)
        y_position += line_height
    
    # Save image
    img.save(save_path)
    print(f"Created placeholder image: {save_path}")
    return True

def fix_missing_product_images():
    """Create placeholder images for products with missing images"""
    app = create_app()
    with app.app_context():
        # Define uploads directory
        uploads_dir = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Get products with images
        products = Product.query.filter(Product.image.isnot(None)).all()
        print(f"Found {len(products)} products with image references")
        
        placeholders_created = 0
        
        for product in products:
            image_name = product.image
            if not image_name:
                continue
            
            # Check if image exists
            image_path = os.path.join(uploads_dir, image_name)
            if os.path.exists(image_path):
                print(f"✅ Image already exists: {image_name}")
                continue
            
            # Create placeholder image
            print(f"Creating placeholder for: {product.name} ({image_name})")
            create_placeholder_image(
                text=product.name, 
                save_path=image_path
            )
            placeholders_created += 1
        
        print(f"\nCreated {placeholders_created} placeholder images")

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
        fix_missing_product_images()
    except ImportError:
        print("Error: PIL/Pillow library not installed. Run: pip install pillow")
