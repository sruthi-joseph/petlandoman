from PIL import Image
import numpy as np
import os

img = Image.open("products & service  image.png")
data = np.array(img)
alpha = data[:, :, 3]
mask = alpha > 0

os.makedirs("extracted_images", exist_ok=True)

# Product X zones
prod_cols = [
    (76, 395),
    (423, 744),
    (787, 1105),
    (1140, 1461)
]

for idx, (x1, x2) in enumerate(prod_cols):
    # Find vertical boundaries in top half (0 to 512)
    sub_mask = mask[0:512, x1:x2]
    row_proj = np.any(sub_mask, axis=1)
    y1 = np.where(row_proj)[0][0]
    y2 = np.where(row_proj)[0][-1]
    
    # Let's crop it with a small margin of 2px
    x1_m = max(0, x1 - 2)
    x2_m = min(1536, x2 + 2)
    y1_m = max(0, y1 - 2)
    y2_m = min(512, y2 + 2)
    
    # We want it to be a perfect square since they are circular images
    w = x2_m - x1_m
    h = y2_m - y1_m
    size = max(w, h)
    cx = (x1_m + x2_m) // 2
    cy = (y1_m + y2_m) // 2
    
    box = (cx - size//2, cy - size//2, cx + size//2, cy + size//2)
    print(f"Product {idx+1} final crop box: {box}")
    img.crop(box).save(f"extracted_images/product_{idx+1}.png")

# Service X zones
svc_cols = [
    (230, 552),
    (654, 969),
    (1214, 1536)
]

for idx, (x1, x2) in enumerate(svc_cols):
    # Find vertical boundaries in bottom half (512 to 1024)
    sub_mask = mask[512:1024, x1:x2]
    row_proj = np.any(sub_mask, axis=1)
    y1 = np.where(row_proj)[0][0] + 512
    y2 = np.where(row_proj)[0][-1] + 512
    
    # Let's crop it exactly (no need for square, just exact fit with minor padding)
    box = (x1 - 2, y1 - 2, x2 + 2, y2 + 2)
    print(f"Service {idx+1} final crop box: {box}")
    img.crop(box).save(f"extracted_images/service_{idx+1}.png")

print("Cropped successfully!")
