import os
from PIL import Image

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_pdf_images\page_8_img_16.png"
out_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

if not os.path.exists(img_path):
    print("Source image not found!")
    exit()

img = Image.open(img_path)
w, h = img.size
print(f"Source size: {w}x{h}")

# Let's crop into 4 cards
# In a 1049x540 image:
# Horizontal split around center (524)
# Vertical split around center (270)
card_w = w // 2
card_h = h // 2

cards = {
    "card_nutritional.png": (0, 0, card_w, card_h),
    "card_obedience.png": (card_w, 0, w, card_h),
    "card_grooming.png": (0, card_h, card_w, h),
    "card_daycare.png": (card_w, card_h, w, h)
}

for name, box in cards.items():
    cropped = img.crop(box)
    cropped.save(os.path.join(out_dir, name))
    print(f"Saved: {name} | Size: {cropped.size}")
