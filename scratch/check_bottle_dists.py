from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg").convert("RGB")
arr = np.array(img)

# Filter out both white background (>240) and cream background (>200 & G>180) to isolate bottle pixels
# Bottle pixels are black / purple / pink / yellow labels / caps
r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

# Cream background is R > 230, G > 215, B > 190
# Dark blue ring is R < 50, G < 60, B < 70 AND radius > 740
height, width, _ = arr.shape
y, x = np.ogrid[:height, :width]
dist = np.sqrt((x - 1200)**2 + (y - 896)**2)

# Bottle pixels: not cream background, not dark ring
is_bg = (r > 220) & (g > 200) & (b > 180)
is_ring = (dist > 740)

is_bottle = (~is_bg) & (~is_ring)

ys, xs = np.where(is_bottle)
print(f"Bottle bounds: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}]")
print(f"Bottle max distance from center (1200, 896):")
dists = np.sqrt((xs - 1200)**2 + (ys - 896)**2)
print(f"Max distance: {dists.max():.1f}px")
print(f"Min X diff: {1200 - xs.min()}, Max X diff: {xs.max() - 1200}")
print(f"Min Y diff: {896 - ys.min()}, Max Y diff: {ys.max() - 896}")
