from PIL import Image
import numpy as np

img_old = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\hygiene suppliments.jpeg").convert("RGB")
img_new = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\product page card-hygiene and supplements.jpeg").convert("RGB")

data_old = np.array(img_old)
data_new = np.array(img_new)

diff = np.abs(data_old.astype(int) - data_new.astype(int))
max_diff = diff.max(axis=2)

# Create a heatmap of diff
diff_vis = np.zeros((1536, 2752, 3), dtype=np.uint8)
diff_vis[max_diff > 30] = [255, 0, 0] # red for differences

# Overlay on gray background of new image
bg = (data_new * 0.5).astype(np.uint8)
bg[max_diff > 30] = [255, 100, 100]

Image.fromarray(bg).resize((800, 446)).save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\diff_overlay.jpg")
print("Saved diff_overlay.jpg")
