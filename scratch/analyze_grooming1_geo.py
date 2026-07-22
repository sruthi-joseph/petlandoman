from PIL import Image, ImageDraw
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
im = Image.open(img_path).convert("RGB")
print("Size:", im.size)

data = np.array(im)
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]

# Find yellow area or non-white area / product bounds
mask_yellow = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask_yellow)
print(f"Yellow pixel count: {len(xs)}")
if len(xs) > 0:
    print(f"Yellow bounding box: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}]")
    cx_yellow = (xs.min() + xs.max()) // 2
    cy_yellow = (ys.min() + ys.max()) // 2
    print(f"Yellow center: ({cx_yellow}, {cy_yellow})")

# Let's also check non-white pixel bounding box
mask_content = (r < 250) | (g < 250) | (b < 250)
ys_c, xs_c = np.where(mask_content)
if len(xs_c) > 0:
    print(f"Content bounding box: X=[{xs_c.min()}, {xs_c.max()}], Y=[{ys_c.min()}, {ys_c.max()}]")
    cx_c = (xs_c.min() + xs_c.max()) // 2
    cy_c = (ys_c.min() + ys_c.max()) // 2
    print(f"Content center: ({cx_c}, {cy_c})")
