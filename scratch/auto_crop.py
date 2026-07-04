from PIL import Image
import numpy as np
import os

# Load image and convert to numpy array to find non-white pixels
img = Image.open("products & service  image.png")
data = np.array(img)

# Convert to grayscale or simple mask of non-white pixels
# Background is pure white (255, 255, 255)
mask = (data[:, :, 0] < 254) | (data[:, :, 1] < 254) | (data[:, :, 2] < 254)

# Create output dir
os.makedirs("extracted_images", exist_ok=True)

# Let's split Row 1 (y from 0 to 512) and Row 2 (y from 512 to 1024)
row1_mask = mask[0:512, :]
row2_mask = mask[512:1024, :]

# For Row 1: We have 4 circles. Let's find their columns by looking at vertical projection.
col_proj1 = np.any(row1_mask, axis=0)
# Find contiguous groups of True values in col_proj1
cols = []
in_group = False
start = 0
for x in range(len(col_proj1)):
    if col_proj1[x] and not in_group:
        start = x
        in_group = True
    elif not col_proj1[x] and in_group:
        cols.append((start, x))
        in_group = False
if in_group:
    cols.append((start, len(col_proj1)))

print("Row 1 Columns detected:", cols)

# Crop Row 1 circles
for idx, (x1, x2) in enumerate(cols):
    # Find y range for this column in row1_mask
    col_mask = row1_mask[:, x1:x2]
    row_proj = np.any(col_mask, axis=1)
    y1 = np.where(row_proj)[0][0]
    y2 = np.where(row_proj)[0][-1]
    
    # We want a square crop for circles
    w = x2 - x1
    h = y2 - y1
    size = max(w, h)
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    
    # Crop box
    box = (cx - size//2, cy - size//2, cx + size//2, cy + size//2)
    print(f"Product {idx+1} box: {box}")
    img.crop(box).save(f"extracted_images/prod{idx+1}.png")

# For Row 2: We have 3 services.
col_proj2 = np.any(row2_mask, axis=0)
cols2 = []
in_group = False
start = 0
for x in range(len(col_proj2)):
    if col_proj2[x] and not in_group:
        start = x
        in_group = True
    elif not col_proj2[x] and in_group:
        if x - start > 10:  # ignore tiny noise
            cols2.append((start, x))
            in_group = False
if in_group:
    cols2.append((start, len(col_proj2)))

print("Row 2 Columns detected:", cols2)

# Crop Row 2 services
for idx, (x1, x2) in enumerate(cols2):
    # Find y range for this column in row2_mask
    col_mask = row2_mask[:, x1:x2]
    row_proj = np.any(col_mask, axis=1)
    y1 = np.where(row_proj)[0][0] + 512
    y2 = np.where(row_proj)[0][-1] + 512
    
    box = (x1, y1, x2, y2)
    print(f"Service {idx+1} box: {box}")
    img.crop(box).save(f"extracted_images/svc{idx+1}.png")

print("Done automatic detection and cropping!")
