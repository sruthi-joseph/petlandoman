from PIL import Image
import numpy as np

img_old = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg").convert("RGB")
img_new = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg").convert("RGB")

data_old = np.array(img_old)
data_new = np.array(img_new)

# Find yellow bounding box for old vs new
for name, data in [("old", data_old), ("new", data_new)]:
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    mask = (r > 175) & (g > 125) & (b < 130)
    ys, xs = np.where(mask)
    print(f"{name} card bounding box: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}], width={xs.max()-xs.min()+1}, height={ys.max()-ys.min()+1}")

# Compare pixels inside the card vs outside the card
r_o, g_o, b_o = data_old[:,:,0], data_old[:,:,1], data_old[:,:,2]
mask_card = (r_o > 175) & (g_o > 125) & (b_o < 130)

diff = np.abs(data_old.astype(int) - data_new.astype(int))
max_diff = diff.max(axis=2)

diff_in_card = max_diff * mask_card
diff_out_card = max_diff * (~mask_card)

print(f"Max diff inside yellow card: {diff_in_card.max()}")
print(f"Max diff outside yellow card: {diff_out_card.max()}")
print(f"Number of differing pixels outside yellow card (>30): {np.sum(diff_out_card > 30)}")
