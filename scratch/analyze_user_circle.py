from PIL import Image
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food-home.jpeg"
img = Image.open(img_path).convert("RGB")
data = np.array(img)
h, w, c = data.shape
cx, cy = w // 2, h // 2

print(f"Center pixel ({cx}, {cy}) color:", data[cy, cx])

# Scan horizontally through the center (y=cy)
print("\nHorizontal scan at y =", cy)
# Print every 50 pixels
for x in range(0, w, 50):
    print(f"x={x}: {data[cy, x]}")

# Scan vertically through the center (x=cx)
print("\nVertical scan at x =", cx)
for y in range(0, h, 50):
    print(f"y={y}: {data[y, cx]}")
