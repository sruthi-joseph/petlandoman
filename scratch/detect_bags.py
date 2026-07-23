import os
import numpy as np
from PIL import Image

def analyze_image(path):
    with Image.open(path) as img:
        arr = np.array(img.convert("RGB"))
        is_bg = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250)
        is_prod = ~is_bg
        
        # Horizontal projection
        col_proj = np.any(is_prod, axis=0)
        # Find continuous segments of True
        segments = []
        in_segment = False
        start = 0
        for i, val in enumerate(col_proj):
            if val and not in_segment:
                start = i
                in_segment = True
            elif not val and in_segment:
                segments.append((start, i - 1))
                in_segment = False
        if in_segment:
            segments.append((start, len(col_proj) - 1))
            
        print(f"  File: {os.path.basename(path)}")
        print(f"    Product bbox width segments: {segments}")
        print(f"    Number of segments: {len(segments)}")

print("HAIRBALL:")
for f in ["26297.webp", "26298.webp", "26302.webp"]:
    analyze_image(os.path.join(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL", f))

print("\nKITTEN:")
for f in ["36812.webp", "36813.webp", "36814.webp"]:
    analyze_image(os.path.join(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN", f))

print("\nMAXI:")
for f in ["25489.webp", "25490.webp", "25493.webp"]:
    analyze_image(os.path.join(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI", f))
