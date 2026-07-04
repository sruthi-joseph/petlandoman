from PIL import Image
import numpy as np

img = Image.open("products & service  image.png")
data = np.array(img)

# Let's count pixels that are not white (i.e. distance from white > 10)
# dist = sqrt((r-255)^2 + (g-255)^2 + (b-255)^2)
white_dist = np.sqrt((data[:, :, 0] - 255.0)**2 + (data[:, :, 1] - 255.0)**2 + (data[:, :, 2] - 255.0)**2)
mask = white_dist > 15

# Split row 1 and row 2
row1_mask = mask[0:512, :]
row2_mask = mask[512:1024, :]

col_sums1 = np.sum(row1_mask, axis=0)
col_sums2 = np.sum(row2_mask, axis=0)

# Let's print columns where sum is high or low
print("Row 1 Column Sums (non-zero zones):")
in_zone = False
start = 0
for x in range(len(col_sums1)):
    # threshold of 5 pixels to avoid small noise
    if col_sums1[x] > 5 and not in_zone:
        start = x
        in_zone = True
    elif col_sums1[x] <= 5 and in_zone:
        print(f"Zone from {start} to {x} (width {x - start}), max sum: {np.max(col_sums1[start:x])}")
        in_zone = False
if in_zone:
    print(f"Zone from {start} to {len(col_sums1)} (width {len(col_sums1) - start})")

print("\nRow 2 Column Sums (non-zero zones):")
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
