from PIL import Image, ImageDraw
import numpy as np

def create_glass_card_bg(width, height, radius, opacity=0.15, filename="assets/glass_card.png"):
    """
    Creates a rounded rectangle image with a white fill at specified opacity.
    """
    # Create valid size image (RGBA)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Calculate color with opacity
    alpha = int(255 * opacity)
    fill_color = (255, 255, 255, alpha)
    
    # Draw rounded rectangle
    draw.rounded_rectangle([(0, 0), (width, height)], radius=radius, fill=fill_color)
    
    print(f"Saving asset to {filename}")
    img.save(filename)

def create_gradient_bg(width, height, c1_hex, c2_hex, filename="assets/bg_gradient.png"):
    """
    Creates a vertical gradient background.
    """
    base = Image.new('RGB', (width, height), c1_hex)
    top = Image.new('RGB', (width, height), c2_hex)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        # 0 to 255
        mask_data.extend([int(255 * (y / height))] * width)
        
    mask.putdata(mask_data)
    
    # Composite
    base.paste(top, (0, 0), mask)
    print(f"Saving bg to {filename}")
    base.save(filename)

if __name__ == "__main__":
    import os
    if not os.path.exists("assets"):
        os.makedirs("assets")
        
    # 1. Glass Card (15% white as requested by user, previous was 10%)
    create_glass_card_bg(600, 400, 20, opacity=0.15, filename="assets/glass_card.png")
    
    # 2. Gradient Background
    # #0F172A to #1E293B
    create_gradient_bg(1600, 900, "#0F172A", "#1E293B", filename="assets/bg_gradient.png")
    
    print("Assets updated.")
