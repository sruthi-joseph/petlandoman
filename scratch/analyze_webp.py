import os
import numpy as np
from PIL import Image

product_folders = {
    "HAIRBALL": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL",
    "KITTEN": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN",
    "MAXI": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI"
}

for name, folder in product_folders.items():
    print(f"\nFolder: {name}")
    if os.path.exists(folder):
        for f in os.listdir(folder):
            if not f.lower().endswith(".webp"):
                continue
            fpath = os.path.join(folder, f)
            with Image.open(fpath) as img:
                img_rgb = img.convert("RGB")
                arr = np.array(img_rgb)
                # Count pixels that are not close to white (e.g., threshold < 250 on all channels)
                # or not exactly white
                not_white = (arr[:, :, 0] < 254) | (arr[:, :, 1] < 254) | (arr[:, :, 2] < 254)
                ys, xs = np.where(not_white)
                if len(xs) > 0 and len(ys) > 0:
                    w = xs.max() - xs.min() + 1
                    h = ys.max() - ys.min() + 1
                    print(f"  {f}: non-white bbox: X=[{xs.min()}, {xs.max()}], Y=[{ys.min()}, {ys.max()}], size=({w}x{h}), aspect={w/h:.3f}")
                else:
                    print(f"  {f}: entirely white!")
