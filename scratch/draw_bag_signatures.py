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
                arr = np.array(img.convert("RGB"))
                
                # Check for white background (pixels near [255, 255, 255])
                is_bg = (arr[:, :, 0] > 250) & (arr[:, :, 1] > 250) & (arr[:, :, 2] > 250)
                is_prod = ~is_bg
                
                # Calculate color statistics for the product pixels
                prod_pixels = arr[is_prod]
                if len(prod_pixels) > 0:
                    avg_color = prod_pixels.mean(axis=0)
                    # Let's count specific color signatures:
                    # Pink (for Kitten): high R, lower G, medium B (e.g. R > 150, G < 120, B > 120)
                    is_pink = (prod_pixels[:, 0] > 150) & (prod_pixels[:, 1] < 120) & (prod_pixels[:, 2] > 120)
                    pink_pct = is_pink.mean() * 100
                    
                    # Blue (for Maxi): high B, lower R (e.g. B > 130, R < 120)
                    is_blue = (prod_pixels[:, 2] > 130) & (prod_pixels[:, 0] < 120)
                    blue_pct = is_blue.mean() * 100
                    
                    # Grey (for Hairball): R, G, B very close to each other, and medium brightness (e.g. max diff < 15, 80 < R < 180)
                    diffs = np.max(prod_pixels, axis=1) - np.min(prod_pixels, axis=1)
                    is_grey = (diffs < 15) & (prod_pixels[:, 0] > 80) & (prod_pixels[:, 0] < 180)
                    grey_pct = is_grey.mean() * 100
                    
                    print(f"  {f}: shape={arr.shape}, avg_color={avg_color.round(1)}")
                    print(f"    Pink%: {pink_pct:.1f}%, Blue%: {blue_pct:.1f}%, Grey%: {grey_pct:.1f}%")
                else:
                    print(f"  {f}: entirely white!")
