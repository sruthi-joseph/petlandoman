import os
import shutil
from PIL import Image, ImageDraw
import numpy as np

new_card_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"
dest_png = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_food_new.png"
old_card_src = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"

target_w = 800
target_h = 446
radius = 40

im = Image.open(new_card_src).convert("RGB")
data = np.array(im)
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

mask = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask)
if len(xs) > 0 and len(ys) > 0:
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    cropped = im.crop((x_min, y_min, x_max + 1, y_max + 1))
else:
    cropped = im

src_w, src_h = cropped.size
target_ratio = target_w / target_h
src_ratio = src_w / src_h

if src_ratio > target_ratio:
    new_w = int(target_ratio * src_h)
    offset = (src_w - new_w) // 2
    cropped_ratio = cropped.crop((offset, 0, offset + new_w, src_h))
else:
    new_h = int(src_w / target_ratio)
    offset = (src_h - new_h) // 2
    cropped_ratio = cropped.crop((0, offset, src_w, offset + new_h))

resized = cropped_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)

alpha_mask = Image.new("L", (target_w, target_h), 0)
draw = ImageDraw.Draw(alpha_mask)
draw.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)

resized.putalpha(alpha_mask)
resized.save(dest_png, "PNG")
print(f"Updated {dest_png} (Size: {resized.size}, Mode: {resized.mode})")

shutil.copy2(new_card_src, old_card_src)
print(f"Updated {old_card_src} with new source image.")
