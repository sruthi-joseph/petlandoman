from PIL import Image
import numpy as np

for name in ["landing banner-pet products.png", "landing banner-pet services.png"]:
    p = rf"c:\Users\SRUTHI\Desktop\petland oman\assets\images\{name}"
    img = Image.open(p).convert("RGB")
    data = np.array(img)
    h, w, c = data.shape
    
    # We want to find the bounding box of the orange-yellow banner.
    # The background is white (255, 255, 255) or very close to white.
    # Let's count pixels that are NOT white.
    # Let's say a pixel is non-white if at least one of R, G, B < 250 (since white is 255, 255, 255).
    non_white = (data[:, :, 0] < 250) | (data[:, :, 1] < 250) | (data[:, :, 2] < 250)
    ys, xs = np.where(non_white)
    
    if len(xs) > 0 and len(ys) > 0:
        x_min, x_max = xs.min(), xs.max()
        y_min, y_max = ys.min(), ys.max()
        print(f"File: {name}")
        print(f"  Shape: {data.shape}")
        print(f"  Non-white bounds: X=[{x_min}, {x_max}], Y=[{y_min}, {y_max}]")
        print(f"  Margin: left={x_min}, right={w - 1 - x_max}, top={y_min}, bottom={h - 1 - y_max}")
    else:
        print(f"File: {name} - No non-white pixels found!")
