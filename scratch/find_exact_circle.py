import numpy as np
from PIL import Image

# Load the image
img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img)

# Let's inspect the center of the image.
# We know the center of the circle might be around (w//2, h//2) or we can search for it.
# Let's search for the golden border.
# The golden border in RGB is typically a warm yellow/orange/gold.
# Let's find pixels that match a golden color.
# Let's check the pixel values across a horizontal line through the vertical center (h // 2).
cy = h // 2
print(f"Image dimensions: {w}x{h}, cy={cy}")

# Let's do a search for the circle boundary:
# Let's compute the color difference or gradient between adjacent pixels.
# Let's look at the gradient along the horizontal center line.
row = arr[cy, :, :]
# Compute the diff of RGB values
diffs = np.linalg.norm(np.diff(row, axis=0), axis=1)

# Find indices where diff is significant
significant_indices = np.where(diffs > 10)[0]
print("Indices with significant horizontal gradient along the center line:")
for idx in significant_indices:
    if 300 < idx < 2100:
        print(f"  x={idx}: color={row[idx]} -> {row[idx+1]}, diff={diffs[idx]:.1f}")
