import numpy as np
from PIL import Image

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

cx, cy = 1200, 906
# Let's inspect background pixels in the upper half of the circle (y < 600)
# which is mostly empty background.
print("Background pixels in upper circle:")
for y in range(200, 601, 100):
    for x in range(800, 1601, 200):
        # Check if inside circle
        dist = np.sqrt((x - cx)**2 + (y - cy)**2)
        if dist < 700:
            print(f"  x={x}, y={y} (dist={dist:.1f}): RGB = {arr[y, x]}")
