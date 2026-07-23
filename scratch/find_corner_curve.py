from PIL import Image
import numpy as np

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet products.png"
img = Image.open(p).convert("RGB")
data = np.array(img)
h, w, c = data.shape

# Let's inspect the top-left corner region: y from 21 to 150, x from 23 to 150.
# We want to print for each y, the x where the yellow card starts.
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
card_mask = (r > 200) & (g > 140) & (b < 150)

print("Top-left boundary curve:")
for y in range(21, 120, 5):
    # Find first x in this row that is in card_mask
    xs = np.where(card_mask[y, :])[0]
    if len(xs) > 0:
        first_x = xs[0]
        print(f"y={y}: first_x={first_x} (offset from left={first_x - 23})")
