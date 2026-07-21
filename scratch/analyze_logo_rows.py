import os
import numpy as np
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
logo_trans_path = os.path.join(image_dir, "logo_transparent.png")

img = Image.open(logo_trans_path).convert("RGBA")
arr = np.array(img)
alpha = arr[:, :, 3]

# Compute number of active pixels per row
row_sums = np.sum(alpha > 0, axis=1)

# Find rows where there are active pixels
active_rows = np.where(row_sums > 0)[0]
if len(active_rows) == 0:
    print("No active rows found")
    exit()

print(f"Active rows range: {active_rows[0]} to {active_rows[-1]}")

# Let's print the row profile for the bottom 300 rows where the text resides
# We'll group rows into consecutive blocks of active pixels and gaps (empty rows)
blocks = []
current_block = []
in_block = False

for y in range(img.height):
    has_pixels = row_sums[y] > 0
    if has_pixels:
        if not in_block:
            in_block = True
            current_block = [y]
        else:
            current_block.append(y)
    else:
        if in_block:
            in_block = False
            blocks.append(("active", current_block[0], current_block[-1], len(current_block)))
            current_block = []

if in_block:
    blocks.append(("active", current_block[0], current_block[-1], len(current_block)))

print("\nBlocks of active vertical lines:")
for idx, (type_, start, end, height) in enumerate(blocks):
    print(f"Block {idx}: Rows {start} to {end} (height={height} pixels)")
