import os
import numpy as np
from PIL import Image, ImageDraw

src_new_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg"
src_old_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg"

dest_png = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_hygiene_new.png"
dest_jpg = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_hygiene_new.jpg"

target_w = 800
target_h = 446
radius = 40

# First, get exact yellow bounding box from old card (or new card)
im_old = Image.open(src_old_path).convert("RGB")
data_old = np.array(im_old)
r, g, b = data_old[:,:,0], data_old[:,:,1], data_old[:,:,2]
mask = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask)
x_min, x_max = xs.min(), xs.max()
y_min, y_max = ys.min(), ys.max()

print(f"Using crop box: x_min={x_min}, x_max={x_max}, y_min={y_min}, y_max={y_max}")

# Open the NEW card image provided by user
im_new = Image.open(src_new_path).convert("RGB")

# Crop the new card image with the exact same crop box
cropped = im_new.crop((x_min, y_min, x_max + 1, y_max + 1))

# Aspect ratio crop as in crop_and_transparent.py
src_w, src_h = cropped.size
src_ratio = src_w / src_h
target_ratio = target_w / target_h

if src_ratio > target_ratio:
    new_w = int(target_ratio * src_h)
    offset = (src_w - new_w) // 2
    cropped_to_ratio = cropped.crop((offset, 0, offset + new_w, src_h))
else:
    new_h = int(src_w / target_ratio)
    offset = (src_h - new_h) // 2
    cropped_to_ratio = cropped.crop((0, offset, src_w, offset + new_h))

# Resize to target 800x446
resized = cropped_to_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Create alpha mask with rounded corners (radius=40)
alpha_mask = Image.new("L", (target_w, target_h), 0)
draw = ImageDraw.Draw(alpha_mask)
draw.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)

# Save PNG with alpha channel
resized_png = resized.copy()
resized_png.putalpha(alpha_mask)

# Save test PNG in scratch first to verify
resized_png.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\test_card_hygiene_new.png", "PNG")

# Also save JPG version if needed
resized_jpg = Image.new("RGB", (target_w, target_h), (255, 255, 255))
resized_jpg.paste(resized, (0, 0), alpha_mask)
resized_jpg.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\test_card_hygiene_new.jpg", "JPEG", quality=95)

print("Saved test cropped card images in scratch.")
