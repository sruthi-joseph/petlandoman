import os
from PIL import Image, ImageDraw
import numpy as np

src_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
dest_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_3.png"

# Radius 728px centered at (1200, 896)
cx, cy, r = 1200, 896, 728

img = Image.open(src_path).convert("RGBA")

box = (cx - r, cy - r, cx + r, cy + r)
cropped = img.crop(box)

# High quality circular alpha mask
mask = Image.new("L", (r * 2, r * 2), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, r * 2, r * 2), fill=255)

cropped.putalpha(mask)

# Resize to standard 500x500 RGBA circle
final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
final_img.save(dest_path, "PNG")

print(f"Successfully generated clean product_3.png at: {dest_path}")
print(f"Dimensions: {final_img.size}, Mode: {final_img.mode}")

# Check that NO dark blue pixels exist near the circular border in the generated image
arr = np.array(final_img)
alpha = arr[:,:,3]
rgb = arr[:,:,:3]

# Check pixels with alpha > 128
valid_pixels = rgb[alpha > 128]
dark_pixels = valid_pixels[(valid_pixels[:,0] < 50) & (valid_pixels[:,1] < 60) & (valid_pixels[:,2] < 70)]
print(f"Total valid pixels in circle: {len(valid_pixels)}")
print(f"Dark pixels (<50 RGB) in image (these are the bottle bodies/caps): {len(dark_pixels)}")
