import numpy as np
from PIL import Image

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
cx = 1200

# Let's print values of pixel colors at (cx, y) for y from 50 to 150
for y in range(50, 150):
    r, g, b = img.getpixel((cx, y))
    # Print when it becomes light
    if r > 100:
        print(f"y={y}: R={r}, G={g}, B={b}")
        break
