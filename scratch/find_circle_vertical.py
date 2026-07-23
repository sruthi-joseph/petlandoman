import numpy as np
from PIL import Image

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

cx = 1200
column = arr[:, cx, :]
diffs = np.linalg.norm(np.diff(column, axis=0), axis=1)

print("Top transitions (y from 50 to 300):")
for y in range(50, 300):
    if diffs[y] > 10:
        print(f"  y={y}: color={column[y]} -> {column[y+1]}, diff={diffs[y]:.1f}")

print("\nBottom transitions (y from 1500 to 1750):")
for y in range(1500, 1750):
    if diffs[y] > 10:
        print(f"  y={y}: color={column[y]} -> {column[y+1]}, diff={diffs[y]:.1f}")
