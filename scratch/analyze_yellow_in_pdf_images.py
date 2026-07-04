import os
from PIL import Image
import numpy as np

output_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_pdf_images"
target_names = ["page_8_img_13.jpg", "page_8_img_14.png", "page_8_img_15.png", "page_8_img_16.png", "page_8_img_17.png"]

for name in target_names:
    path = os.path.join(output_dir, name)
    if not os.path.exists(path):
        print(f"{name} does not exist")
        continue
    img = Image.open(path).convert("RGB")
    data = np.array(img)
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    
    # check for fcc203 yellow: (252, 194, 3)
    # let's look for pixels with R > 230, G > 170, B < 40
    yellow_mask = (r > 230) & (g > 170) & (b < 40)
    yellow_pct = np.mean(yellow_mask) * 100
    
    print(f"File: {name} | Size: {img.size}")
    print(f"  Yellow pixel percentage: {yellow_pct:.1f}%")
    if yellow_pct > 1.0:
        # find bounding box of yellow pixels
        ys, xs = np.where(yellow_mask)
        print(f"  Yellow bounds: x={xs.min()} to {xs.max()}, y={ys.min()} to {ys.max()}")
