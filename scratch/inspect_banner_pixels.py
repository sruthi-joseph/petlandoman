from PIL import Image
import os
import numpy as np

banners = [
    r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet products.png",
    r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet services.png",
    r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_products.jpeg",
    r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\banner_for_pet_services.jpeg"
]

for p in banners:
    if os.path.exists(p):
        with Image.open(p) as img:
            print(f"File: {os.path.basename(p)}")
            print(f"  Size: {img.size}")
            print(f"  Mode: {img.mode}")
            print(f"  Format: {img.format}")
    else:
        print(f"File not found: {p}")
