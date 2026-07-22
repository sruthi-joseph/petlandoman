from PIL import Image
import numpy as np

img_new = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg")
print("New pet food card size:", img_new.size, "aspect ratio:", img_new.width / img_new.height)

data_new = np.array(img_new.convert("RGB"))
r, g, b = data_new[:,:,0], data_new[:,:,1], data_new[:,:,2]

# Check corners of pet_food card.jpeg
print("Top-left pixel RGB:", data_new[0, 0])
print("Top-right pixel RGB:", data_new[0, -1])
print("Bottom-left pixel RGB:", data_new[-1, 0])
print("Bottom-right pixel RGB:", data_new[-1, -1])

# Yellow detection
mask_yellow = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask_yellow)
print(f"Yellow pixel count: {len(xs)}")
if len(xs) > 0:
    print(f"Yellow bounding box: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}]")
