from PIL import Image
import numpy as np

img_old = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg")
img_new = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg")

print("Old card image mode & size:", img_old.mode, img_old.size)
print("New card image mode & size:", img_new.mode, img_new.size)

# Let's save a thumbnail or slice of both to scratch to understand what's in them
img_old.resize((800, 446)).save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\old_card_thumb.jpg")
img_new.resize((800, 446)).save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\new_card_thumb.jpg")

print("Thumbnails saved.")
