from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg").convert("RGB")
arr = np.array(img)

# Let's inspect concentric rings from center (1200, 896) outward
cx, cy = 1200, 896
height, width, _ = arr.shape

y, x = np.ogrid[:height, :width]
dist_from_center = np.sqrt((x - cx)**2 + (y - cy)**2)

# Check average color at radius 400, 500, 600, 700, 750, 800, 820, 840, 860, 880
for r_val in [400, 500, 600, 650, 700, 730, 760, 790, 820, 850, 870]:
    mask_ring = (dist_from_center >= r_val - 5) & (dist_from_center <= r_val + 5)
    ring_pixels = arr[mask_ring]
    if len(ring_pixels) > 0:
        mean_rgb = ring_pixels.mean(axis=0)
        print(f"Radius {r_val}px -> Mean RGB: {mean_rgb.round(1)}")
