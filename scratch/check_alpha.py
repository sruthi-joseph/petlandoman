from PIL import Image
import numpy as np

img = Image.open("products & service  image.png")
data = np.array(img)

# Use Alpha channel (index 3)
alpha = data[:, :, 3]
mask = alpha > 0

row1_mask = mask[0:512, :]
row2_mask = mask[512:1024, :]

col_sums1 = np.sum(row1_mask, axis=0)
col_sums2 = np.sum(row2_mask, axis=0)

print("Row 1 Column Sums (non-zero Alpha zones):")
in_zone = False
start = 0
for x in range(len(col_sums1)):
    if col_sums1[x] > 5 and not in_zone:
        start = x
        in_zone = True
    elif col_sums1[x] <= 5 and in_zone:
        print(f"Zone from {start} to {x} (width {x - start}), max sum: {np.max(col_sums1[start:x])}")
        in_zone = False
if in_zone:
    print(f"Zone from {start} to {len(col_sums1)} (width {len(col_sums1) - start})")

print("\nRow 2 Column Sums (non-zero Alpha zones):")
in_zone = False
start = 0
for x in range(len(col_sums2)):
    if col_sums2[x] > 5 and not in_zone:
        start = x
        in_zone = True
    elif col_sums2[x] <= 5 and in_zone:
        print(f"Zone from {start} to {x} (width {x - start}), max sum: {np.max(col_sums2[start:x])}")
        in_zone = False
if in_zone:
    print(f"Zone from {start} to {len(col_sums2)} (width {len(col_sums2) - start})")
