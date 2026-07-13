import os
import numpy as np
from PIL import Image, ImageDraw

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\product card images"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

files_mapping = {
    "pet food.jpeg": "card_prod_food_new.png",
    "toys and fun.jpeg": "card_prod_toys_new.png",
    "hygiene suppliments.jpeg": "card_prod_hygiene_new.png",
    "accessories.jpeg": "card_prod_accessories_new.png"
}

target_w = 800
target_h = 446

for src_name, dest_name in files_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Source file {src_path} not found!")
        continue
        
    im = Image.open(src_path).convert("RGB")
    data = np.array(im)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    
    # Threshold to find the yellow card. The card has bright yellow background.
    # Yellow is high R, high G, low B.
    mask = (r > 175) & (g > 125) & (b < 130)
    ys, xs = np.where(mask)
    
    if len(xs) == 0 or len(ys) == 0:
        print(f"Error: No yellow region found for {src_name}")
        continue
        
    # Crop to the yellow bounding box
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    
    # Crop the image
    cropped = im.crop((x_min, y_min, x_max + 1, y_max + 1))
    print(f"{src_name} cropped to: {cropped.size} (aspect ratio: {cropped.width/cropped.height:.4f})")
    
    # We want to resize it to target_w x target_h (800 x 446)
    # Since aspect ratios might be slightly different, let's crop the cropped image to target aspect ratio
    src_w, src_h = cropped.size
    src_ratio = src_w / src_h
    target_ratio = target_w / target_h
    
    if src_ratio > target_ratio:
        # Crop width (left/right)
        new_w = int(target_ratio * src_h)
        offset = (src_w - new_w) // 2
        cropped_to_ratio = cropped.crop((offset, 0, offset + new_w, src_h))
    else:
        # Crop height (top/bottom)
        new_h = int(src_w / target_ratio)
        offset = (src_h - new_h) // 2
        cropped_to_ratio = cropped.crop((0, offset, src_w, offset + new_h))
        
    # Resize to target
    resized = cropped_to_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Apply rounded corners mask to remove the background at the corners
    # Let's estimate the corner radius. For a card of 800x446, 
    # the original card seems to have corner radius of about 100px in the high-res version, 
    # which is around 30px in the resized 800x446 version. Let's use 35px or 40px.
    # Let's write a mask with radius 40px.
    radius = 40
    alpha_mask = Image.new("L", (target_w, target_h), 0)
    draw = ImageDraw.Draw(alpha_mask)
    draw.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)
    
    # Put the mask into the alpha channel
    resized.putalpha(alpha_mask)
    
    # Save as PNG
    resized.save(dest_path, "PNG")
    print(f"Saved transparent cropped PNG: {dest_path} size: {resized.size}")
