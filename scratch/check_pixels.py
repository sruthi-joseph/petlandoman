import os
from PIL import Image
import numpy as np

path = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images\card_nutritional_opt.jpg"
if os.path.exists(path):
    img = Image.open(path).convert("RGB")
    width, height = img.size
    print(f"Dimensions: {width}x{height}")
    
    # Let's crop the left half (where the text usually sits)
    left_half = img.crop((0, 0, width // 2, height))
    data = np.array(left_half)
    
    # Let's find unique colors or check if there is dark text.
    # The yellow background is around #FCC203 or similar.
    # Let's see how many pixels are dark (e.g., R < 50, G < 50, B < 50)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    dark_pixels = np.sum((r < 80) & (g < 80) & (b < 80))
    print(f"Dark pixels in left half: {dark_pixels} out of {left_half.size[0] * left_half.size[1]}")
    
    # Let's list some unique colors
    # We can also save a small thumbnail or description
else:
    print("File not found")
