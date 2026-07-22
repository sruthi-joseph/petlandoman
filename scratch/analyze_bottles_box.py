from PIL import Image
import numpy as np

img = Image.open(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg").convert("RGB")
arr = np.array(img)

# Non-white pixels (where R, G, B < 240)
mask = (arr[:,:,0] < 240) | (arr[:,:,1] < 240) | (arr[:,:,2] < 240)
ys, xs = np.where(mask)

if len(xs) > 0:
    min_x, max_x = xs.min(), xs.max()
    min_y, max_y = ys.min(), ys.max()
    cx = (min_x + max_x) // 2
    cy = (min_y + max_y) // 2
    w = max_x - min_x + 1
    h = max_y - min_y + 1
    print(f"Products bounding box: X=[{min_x}, {max_x}] (width={w}), Y=[{min_y}, {max_y}] (height={h})")
    print(f"Products center: ({cx}, {cy})")
    
    # Check max radius needed to include all non-white pixels around (cx, cy)
    dist = np.sqrt((xs - cx)**2 + (ys - cy)**2)
    max_r = int(np.ceil(dist.max()))
    print(f"Max distance from center to enclose all product pixels: {max_r}")
