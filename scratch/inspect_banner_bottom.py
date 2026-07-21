import os
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
img_path = os.path.join(image_dir, "banner_for_pet_products.jpeg")

img = Image.open(img_path).convert("RGB")
w, h = img.size
print(f"Image size: {w}x{h}")

# Inspect the bottom row of pixels
arr = np.array(img)
bottom_row = arr[-1, :, :]

# Let's print unique colors in the bottom row or average color
avg_color = np.mean(bottom_row, axis=0)
print(f"Average color of the bottom row: {avg_color}")

# Let's check a few pixels on the bottom left, middle, right
print(f"Bottom-left color (0, {h-1}): {img.getpixel((0, h-1))}")
print(f"Bottom-middle color ({w//2}, {h-1}): {img.getpixel((w//2, h-1))}")
print(f"Bottom-right color ({w-1}, {h-1}): {img.getpixel((w-1, h-1))}")

# Let's also check color at (w//2, h-10) to see if it is uniform
print(f"Color at ({w//2}, {h-10}): {img.getpixel((w//2, h-10))}")
