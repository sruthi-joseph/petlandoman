import os
from PIL import Image
import numpy as np

path = r"c:\Users\SRUTHI\Desktop\petland oman\pet food.jpeg"
if os.path.exists(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size
    print(f"Dimensions: {width}x{height}")
    
    # Check the leftmost column area (x from 0 to 300) where text would be
    leftmost = img.crop((0, 0, 300, height))
    data = np.array(leftmost)
    
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    # Check for non-black pixels (brightness > 20)
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    non_black = np.sum(brightness > 20)
    total = leftmost.size[0] * leftmost.size[1]
    print(f"Non-black pixels in far-left (0-300px): {non_black} out of {total} ({non_black / total * 100:.2f}%)")
else:
    print("File not found")
