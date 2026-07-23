import os
from PIL import Image

kitten_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN"

for f in ["36812.webp", "36813.webp", "36814.webp"]:
    p = os.path.join(kitten_dir, f)
    with Image.open(p) as img:
        print(f"File: {f}, Size: {img.size}")
        # Crop to bounding box of non-white pixels
        rgba = img.convert("RGBA")
        bbox = rgba.getbbox()
        print(f"  bbox: {bbox}")
