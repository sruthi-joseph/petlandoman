import os
from PIL import Image
import numpy as np

path = r"c:\Users\SRUTHI\Desktop\petland oman\pet food.jpeg"
if os.path.exists(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size
    print(f"Dimensions: {width}x{height}")
    
    # Check left half (e.g. x from 0 to width // 2)
    left_half = img.crop((0, 0, width // 2, height))
    data = np.array(left_half)
    
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    # Check how many pixels are completely black or very close to black (R < 15, G < 15, B < 15)
    black_pixels = np.sum((r < 15) & (g < 15) & (b < 15))
    total_left = left_half.size[0] * left_half.size[1]
    print(f"Very dark pixels in left half: {black_pixels} out of {total_left} ({black_pixels / total_left * 100:.2f}%)")
else:
    print("File not found")
