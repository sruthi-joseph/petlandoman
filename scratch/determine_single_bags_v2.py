import os
import numpy as np
from PIL import Image

segmented_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\segmented"

for f in sorted(os.listdir(segmented_dir)):
    if f.endswith(".png"):
        p = os.path.join(segmented_dir, f)
        with Image.open(p) as img:
            arr = np.array(img)
            # Alpha channel is channel 3
            alpha = arr[:, :, 3]
            is_prod = alpha > 0
            
            ys, xs = np.where(is_prod)
            w = xs.max() - xs.min() + 1
            h = ys.max() - ys.min() + 1
            
            h_10 = int(ys.min() + h * 0.1)
            h_50 = int(ys.min() + h * 0.5)
            h_90 = int(ys.min() + h * 0.9)
            
            w_10 = np.sum(is_prod[h_10, :])
            w_50 = np.sum(is_prod[h_50, :])
            w_90 = np.sum(is_prod[h_90, :])
            
            print(f"File: {f} (size: {w}x{h}, aspect: {w/h:.3f})")
            print(f"  Width at 10% height: {w_10}")
            print(f"  Width at 50% height: {w_50}")
            print(f"  Width at 90% height: {w_90}")
            print(f"  Ratio 10%/50%: {w_10/w_50:.2f}, Ratio 90%/50%: {w_90/w_50:.2f}")
