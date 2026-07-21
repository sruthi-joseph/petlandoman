import os
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

img_path = os.path.join(image_dir, "banner_for_pet_products.jpeg")
img = Image.open(img_path).convert("RGB")
w, h = img.size

padding = 70
new_h = h + padding

# Create new image
new_img = Image.new("RGB", (w, new_h))
# Paste original image at top
new_img.paste(img, (0, 0))

# Extend the last row of pixels downwards
pixels = new_img.load()
for x in range(w):
    color = pixels[x, h - 1]
    for y in range(h, new_h):
        pixels[x, y] = color

# Save to artifacts for inspection
new_img.save(os.path.join(artifact_dir, "banner_products_extended.jpeg"), format="JPEG")
print(f"Saved extended banner to artifacts: new size = {w}x{new_h}")
