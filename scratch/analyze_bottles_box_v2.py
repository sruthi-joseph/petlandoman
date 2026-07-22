from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg").convert("RGB")
arr = np.array(img)

# Check histogram or threshold for the bottles
mask = (arr[:,:,0] < 220) | (arr[:,:,1] < 220) | (arr[:,:,2] < 220)
ys, xs = np.where(mask)

if len(xs) > 0:
    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    print(f"Threshold < 220 Products box: X=[{min_x}, {max_x}] (w={w}), Y=[{min_y}, {max_y}] (h={h})")
    print(f"Center: ({cx}, {cy})")
