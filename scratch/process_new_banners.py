from PIL import Image, ImageDraw
import os

# New banners provided by user
products_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet products.png"
services_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet services.png"

# Destination PNG banners
products_dest = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_products.png"
services_dest = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_services.png"

# 1. Process Products Banner
# Bounding box coordinates: X=[23, 2070], Y=[21, 717]
# Width = 2048, Height = 697
if os.path.exists(products_src):
    img = Image.open(products_src).convert("RGBA")
    box = (23, 21, 2070, 717)
    cropped = img.crop(box)
    w_c, h_c = cropped.size
    
    # Create smooth anti-aliased rounded rectangle mask
    radius = 70
    factor = 4
    mask_large = Image.new("L", (w_c * factor, h_c * factor), 0)
    draw_large = ImageDraw.Draw(mask_large)
    draw_large.rounded_rectangle((0, 0, w_c * factor, h_c * factor), radius * factor, fill=255)
    
    mask = mask_large.resize((w_c, h_c), Image.Resampling.LANCZOS)
    cropped.putalpha(mask)
    cropped.save(products_dest, "PNG")
    print(f"Processed and saved products banner: {products_dest}")
else:
    print(f"Error: {products_src} not found!")

# 2. Process Services Banner
# Bounding box coordinates: X=[31, 2061], Y=[35, 700]
# Width = 2030, Height = 666
if os.path.exists(services_src):
    img = Image.open(services_src).convert("RGBA")
    box = (31, 35, 2061, 700)
    cropped = img.crop(box)
    w_c, h_c = cropped.size
    
    # Create smooth anti-aliased rounded rectangle mask
    radius = 70
    factor = 4
    mask_large = Image.new("L", (w_c * factor, h_c * factor), 0)
    draw_large = ImageDraw.Draw(mask_large)
    draw_large.rounded_rectangle((0, 0, w_c * factor, h_c * factor), radius * factor, fill=255)
    
    mask = mask_large.resize((w_c, h_c), Image.Resampling.LANCZOS)
    cropped.putalpha(mask)
    cropped.save(services_dest, "PNG")
    print(f"Processed and saved services banner: {services_dest}")
else:
    print(f"Error: {services_src} not found!")
