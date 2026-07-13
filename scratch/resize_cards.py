import os
from PIL import Image

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\product card images"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

files_mapping = {
    "pet food.jpeg": "card_prod_food_new.jpg",
    "toys and fun.jpeg": "card_prod_toys_new.jpg",
    "hygiene suppliments.jpeg": "card_prod_hygiene_new.jpg",
    "accessories.jpeg": "card_prod_accessories_new.jpg"
}

target_w = 800
target_h = 446

for src_name, dest_name in files_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Source file {src_path} not found!")
        continue
        
    im = Image.open(src_path)
    # Check dimensions
    w, h = im.size
    print(f"Original {src_name}: {w}x{h}")
    
    # We want to resize it. Since aspect ratio is 1.7916 and 800/446 is 1.7937,
    # let's crop slightly if needed, or just resize directly.
    # To keep exact aspect ratio, let's crop the source image to target aspect ratio:
    src_ratio = w / h
    target_ratio = target_w / target_h
    
    if src_ratio > target_ratio:
        # Source is wider, crop left/right
        new_w = int(target_ratio * h)
        offset = (w - new_w) // 2
        im_cropped = im.crop((offset, 0, offset + new_w, h))
    else:
        # Source is taller, crop top/bottom
        new_h = int(w / target_ratio)
        offset = (h - new_h) // 2
        im_cropped = im.crop((0, offset, w, offset + new_h))
        
    # Now resize to target dimensions
    im_resized = im_cropped.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # Save as compressed JPEG
    im_resized.convert("RGB").save(dest_path, "JPEG", quality=85)
    print(f"Saved optimized image to {dest_path} | Size: {im_resized.size}")
