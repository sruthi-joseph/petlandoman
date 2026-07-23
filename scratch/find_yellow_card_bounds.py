from PIL import Image
import numpy as np

for name in ["landing banner-pet products.png", "landing banner-pet services.png"]:
    p = rf"c:\Users\SRUTHI\Desktop\petland oman\assets\images\{name}"
    img = Image.open(p).convert("RGB")
    data = np.array(img)
    h, w, c = data.shape
    
    # We want to identify the yellow/orange pixels.
    # Yellow/orange pixels have high R and G, and low B.
    # From our row scans, inside the card, R > 200, G > 150, B < 150.
    # Let's write a conservative check: R > 200 and G > 140 and B < 150.
    # Let's count how many pixels match this in each row/column to find the card edges.
    r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
    card_mask = (r > 200) & (g > 140) & (b < 150)
    
    ys, xs = np.where(card_mask)
    if len(xs) > 0 and len(ys) > 0:
        print(f"\n=== {name} ===")
        print(f"Yellow mask bounds: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}]")
        # Let's check the color just outside and inside the detected Y min
        ymin = ys.min()
        print(f"y={ymin-1} at x=1000: {data[ymin-1, 1000]}")
        print(f"y={ymin} at x=1000: {data[ymin, 1000]}")
        xmin = xs.min()
        print(f"x={xmin-1} at y=374: {data[374, xmin-1]}")
        print(f"x={xmin} at y=374: {data[374, xmin]}")
        xmax = xs.max()
        print(f"x={xmax} at y=374: {data[374, xmax]}")
        print(f"x={xmax+1} at y=374: {data[374, xmax+1]}")
        ymax = ys.max()
        print(f"y={ymax} at x=1000: {data[ymax, 1000]}")
        print(f"y={ymax+1} at x=1000: {data[ymax+1, 1000]}")
