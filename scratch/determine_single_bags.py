import os
import numpy as np
from PIL import Image

def analyze_profile(name, folder, filename):
    p = os.path.join(folder, filename)
    with Image.open(p) as img:
        arr = np.array(img.convert("RGB"))
        is_bg = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250)
        is_prod = ~is_bg
        
        ys, xs = np.where(is_prod)
        if len(xs) == 0 or len(ys) == 0:
            print(f"{filename}: empty")
            return
            
        x1, x2 = xs.min(), xs.max()
        y1, y2 = ys.min(), ys.max()
        
        w = x2 - x1 + 1
        h = y2 - y1 + 1
        
        # Calculate width of the product at 10%, 50%, and 90% of its height
        h_10 = int(y1 + h * 0.1)
        h_50 = int(y1 + h * 0.5)
        h_90 = int(y1 + h * 0.9)
        
        w_10 = np.sum(is_prod[h_10, :])
        w_50 = np.sum(is_prod[h_50, :])
        w_90 = np.sum(is_prod[h_90, :])
        
        print(f"File: {name}/{filename} (size: {w}x{h}, aspect: {w/h:.3f})")
        print(f"  Width at 10% height: {w_10}")
        print(f"  Width at 50% height: {w_50}")
        print(f"  Width at 90% height: {w_90}")
        print(f"  Ratio 10%/50%: {w_10/w_50:.2f}, Ratio 90%/50%: {w_90/w_50:.2f}")

product_folders = {
    "HAIRBALL": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL",
    "KITTEN": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN",
    "MAXI": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI"
}

for name, folder in product_folders.items():
    print(f"\nCategory: {name}")
    for f in sorted(os.listdir(folder)):
        if f.endswith(".webp"):
            analyze_profile(name, folder, f)
