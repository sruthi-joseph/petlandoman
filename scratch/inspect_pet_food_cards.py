import os
from PIL import Image

new_img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"
old_img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
card_prod_food_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_food_new.png"

for name, p in [("pet_food card.jpeg", new_img_path), ("pet food.jpeg", old_img_path), ("card_prod_food_new.png", card_prod_food_path)]:
    if os.path.exists(p):
        im = Image.open(p)
        print(f"File: {name}, Size: {im.size}, Mode: {im.mode}")
    else:
        print(f"File NOT found: {p}")
