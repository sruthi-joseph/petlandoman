import os
from PIL import Image
import numpy as np

img_names = ["pet food.jpeg", "toys & fun.jpeg", "groomin products.jpeg", "accessories.jpeg"]
base_dir = r"c:\Users\SRUTHI\Desktop\petland oman"

for name in img_names:
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        print(f"{name} not found")
        continue
    img = Image.open(path).convert("RGB")
    width, height = img.size
    print(f"Image: {name} | Dimensions: {width}x{height}")
    
    # Check if background is dark/black (R < 30, G < 30, B < 30)
    data = np.array(img)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    dark_pixels = np.sum((r < 30) & (g < 30) & (b < 30))
    total_pixels = width * height
    print(f"  Dark pixels: {dark_pixels} / {total_pixels} ({dark_pixels / total_pixels * 100:.2f}%)")
