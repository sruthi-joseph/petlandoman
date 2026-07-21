import os
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
img_path = os.path.join(image_dir, "banner_for_pet_products.jpeg")

img = Image.open(img_path).convert("RGB")
w, h = img.size

# Let's inspect the last 30 rows at X = w // 2 (middle)
print("Middle vertical profile (last 30 rows):")
for y in range(h - 30, h):
    print(f"y={y}: {img.getpixel((w//2, y))}")

# Let's inspect the left side to see where the white border turns yellow
print("\nLeft border check (X=0, last 30 rows):")
for y in range(h - 30, h):
    print(f"y={y}: {img.getpixel((0, y))}")

# Let's inspect the right side
print("\nRight border check (X=w-1, last 30 rows):")
for y in range(h - 30, h):
    print(f"y={y}: {img.getpixel((w-1, y))}")
