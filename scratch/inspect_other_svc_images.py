import os
from PIL import Image
import numpy as np

img_names = ["service_1.png", "service_2.png", "service_3.png", "svc1.png", "svc2.png", "svc3.png"]
base_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

for name in img_names:
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        print(f"{name} not found!")
        continue
    img = Image.open(path).convert("RGBA")
    data = np.array(img)
    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
    
    # check if there are white pixels
    white_opaque = np.sum((r == 255) & (g == 255) & (b == 255) & (a == 255))
    white_any_alpha = np.sum((r == 255) & (g == 255) & (b == 255) & (a > 0))
    
    print(f"Image: {name} | Size: {img.size}")
    print(f"  Opaque white pixels: {white_opaque}")
    print(f"  Any-alpha white pixels: {white_any_alpha}")
