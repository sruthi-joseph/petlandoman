import os
from PIL import Image

src_img = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
prod_3_img = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_3.png"

for name, p in [("grooming-products1.jpeg", src_img), ("product_3.png", prod_3_img)]:
    if os.path.exists(p):
        im = Image.open(p)
        print(f"File: {name}, Size: {im.size}, Mode: {im.mode}")
    else:
        print(f"File NOT found: {p}")
