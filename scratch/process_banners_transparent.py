from PIL import Image, ImageDraw
import os

# New banners provided by user
products_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet products.png"
services_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet services.png"

# Destination PNG banners
products_dest = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_products.png"
services_dest = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_services.png"

def process_banner(src_path, dest_path, box, radius):
    if not os.path.exists(src_path):
        print(f"Error: {src_path} not found!")
        return
        
    img = Image.open(src_path).convert("RGBA")
    w, h = img.size
    
    # Create mask of the same size as original image (transparent everywhere)
    mask = Image.new("L", (w, h), 0)
    
    # Coordinates of the card
    xmin, ymin, xmax, ymax = box
    w_card = xmax - xmin
    h_card = ymax - ymin
    
    # Draw rounded rectangle for the card inside the mask
    # We do it with supersampling (factor=4) to ensure smooth edges
    factor = 4
    mask_large = Image.new("L", (w * factor, h * factor), 0)
    draw_large = ImageDraw.Draw(mask_large)
    
    # Draw rounded rectangle at position (xmin * factor, ymin * factor)
    draw_large.rounded_rectangle(
        (xmin * factor, ymin * factor, xmax * factor, ymax * factor),
        radius * factor,
        fill=255
    )
    
    # Resize mask back to original size
    mask = mask_large.resize((w, h), Image.Resampling.LANCZOS)
    
    # Apply mask to image
    img.putalpha(mask)
    
    # Save as PNG
    img.save(dest_path, "PNG")
    print(f"Processed and saved transparent banner: {dest_path} (Size: {img.size})")

# Products: box=(23, 21, 2070, 717), radius=70
process_banner(products_src, products_dest, (23, 21, 2070, 717), 70)

# Services: box=(31, 35, 2061, 700), radius=70
process_banner(services_src, services_dest, (31, 35, 2061, 700), 70)
