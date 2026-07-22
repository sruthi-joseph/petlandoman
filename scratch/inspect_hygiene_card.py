import os
from PIL import Image
import numpy as np

img1_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg"
img2_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg"
card_prod_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_hygiene_new.png"

for p in [img1_path, img2_path, card_prod_path]:
    if os.path.exists(p):
        im = Image.open(p)
        print(f"File: {os.path.basename(p)}, Size: {im.size}, Mode: {im.mode}")
    else:
        print(f"File NOT found: {p}")
