import os
from PIL import Image, ImageDraw

src_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
dest_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_3.png"

# Radius 860 centered at (1200, 896)
cx, cy, r = 1200, 896, 860

img = Image.open(src_path).convert("RGBA")

# Crop to square bounding box
box = (cx - r, cy - r, cx + r, cy + r)
cropped = img.crop(box)

# High-resolution circular mask with anti-aliasing
mask = Image.new("L", (r * 2, r * 2), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, r * 2, r * 2), fill=255)

cropped.putalpha(mask)

# Resize to standard 500x500 high-res circle PNG
final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
final_img.save(dest_path, "PNG")

print(f"Successfully generated: {dest_path}")
print(f"Mode: {final_img.mode}, Size: {final_img.size}")
