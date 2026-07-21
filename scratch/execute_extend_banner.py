import os
import shutil
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
img_path = os.path.join(image_dir, "banner_for_pet_products.jpeg")
backup_path = os.path.join(image_dir, "banner_for_pet_products_backup_clip.jpeg")

# 1. Create backup
print("1. Creating backup of banner image...")
shutil.copy2(img_path, backup_path)
print(f"Backup created at: {backup_path}")

# 2. Modify image in place
print("\n2. Modifying banner image in place...")
img = Image.open(img_path).convert("RGB")
w, h = img.size
print(f"Original dimensions: {w}x{h}")

padding = 70
new_h = h + padding

# Create new image canvas
new_img = Image.new("RGB", (w, new_h))
new_img.paste(img, (0, 0))

# Extend the last row of pixels downwards to fill the padded area
pixels = new_img.load()
for x in range(w):
    color = pixels[x, h - 1]
    for y in range(h, new_h):
        pixels[x, y] = color

# Save modified image in place
new_img.save(img_path, format="JPEG")
print(f"Modified image saved to: {img_path}")
print(f"New dimensions: {new_img.size}")
