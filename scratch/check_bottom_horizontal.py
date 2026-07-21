import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
img_path = os.path.join(image_dir, "banner_for_pet_products.jpeg")

img = Image.open(img_path).convert("RGB")
w, h = img.size

# Check row h - 1 (y=875) from left edge X=0 to X=100
print("Left corner transition on y=875:")
for x in range(100):
    color = img.getpixel((x, h - 1))
    # print only if it's changing or every few steps
    print(f"x={x}: {color}")
