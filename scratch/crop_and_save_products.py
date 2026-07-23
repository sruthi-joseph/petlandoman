import os
import numpy as np
from PIL import Image

output_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\cropped_products"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
                
                # Check background color by looking at top-left corner
                bg_color = arr[0, 0]
                print(f"  {f}: bg_color={bg_color}")
                
                # Threshold to detect non-background pixels.
                # If bg is white, diff from [255, 255, 255]
                diff = np.linalg.norm(arr - bg_color, axis=2)
                mask = diff > 15
                
                ys, xs = np.where(mask)
                if len(xs) > 0 and len(ys) > 0:
                    x_min, x_max = xs.min(), xs.max()
                    y_min, y_max = ys.min(), ys.max()
                    
                    cropped = img_rgb.crop((x_min, y_min, x_max + 1, y_max + 1))
                    out_path = os.path.join(output_dir, f"{name}_{f}")
                    cropped.save(out_path)
                    print(f"    Saved cropped {f} to {out_path} (size: {cropped.size})")
                else:
                    print(f"    {f} is entirely background color!")
