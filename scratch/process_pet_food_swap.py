import os
import shutil
import numpy as np
from PIL import Image, ImageDraw

new_card_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"
old_card_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"

dest_png = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_food_new.png"

target_w = 800
target_h = 446
radius = 40

# Load old card to get the precise card bounding box
im_old = Image.open(old_card_src).convert("RGB")
data_old = np.array(im_old)
r, g, b = data_old[:,:,0], data_old[:,:,1], data_old[:,:,2]
mask = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask)
x_min, x_max = xs.min(), xs.max()
y_min, y_max = ys.min(), ys.max()

print(f"Old Pet Food card crop box bounds: X=[{x_min}, {x_max}], Y=[{y_min}, {y_max}]")

# Also check yellow region on new image
im_new = Image.open(new_card_src).convert("RGB")
data_new = np.array(im_new)
rn, gn, bn = data_new[:,:,0], data_new[:,:,1], data_new[:,:,2]
mask_n = (rn > 175) & (gn > 125) & (bn < 130)
ys_n, xs_n = np.where(mask_n)
if len(xs_n) > 0 and len(ys_n) > 0:
    print(f"New Pet Food card yellow bounds: X=[{xs_n.min()}, {xs_n.max()}], Y=[{ys_n.min()}, {ys_n.max()}]")

# Crop the new card image
cropped = im_new.crop((x_min, y_min, x_max + 1, y_max + 1))

# Match aspect ratio to target_w / target_h
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

# High quality resize
resized = cropped_to_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)

# Create rounded corners alpha mask (radius 40px)
alpha_mask = Image.new("L", (target_w, target_h), 0)
draw = ImageDraw.Draw(alpha_mask)
draw.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)

# Put alpha mask
resized.putalpha(alpha_mask)

# Save to extracted_images/card_prod_food_new.png
resized.save(dest_png, "PNG")
print(f"Successfully updated: {dest_png}")

# Also update pet food.jpeg with new image file
shutil.copy2(new_card_src, old_card_src)
print(f"Updated {old_card_src} with new card image source.")
