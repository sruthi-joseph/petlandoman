from PIL import Image
import numpy as np

for name in ["landing banner-pet products.png", "landing banner-pet services.png"]:
    p = rf"c:\Users\SRUTHI\Desktop\petland oman\assets\images\{name}"
    img = Image.open(p).convert("RGB")
    data = np.array(img)
    h, w, c = data.shape
    
    # Let's inspect pixel colors at y=10, 50, 100, 200, 374
    # print the first 100 pixels color to see where it transitions from the light cream color
    print(f"\n=== {name} ===")
    for y in [10, 50, 100, 200, 374]:
        # Let's print x=0, 10, 20, ..., 150
        print(f"y={y}:")
        row = []
        for x in range(0, 150, 10):
            row.append(f"x={x}:({data[y,x,0]},{data[y,x,1]},{data[y,x,2]})")
        print("  ".join(row))
