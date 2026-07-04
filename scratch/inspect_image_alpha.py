from PIL import Image
import os
import numpy as np

dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
images = ["grooming_shower.png", "grooming_haircut.png", "grooming_deshedding.png", "grooming_full.png", "grooming_medicated.png"]

for name in images:
    path = os.path.join(dest_dir, name)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"Image: {name} | Size: {img.size} | Mode: {img.mode}")
        if img.mode == "RGBA":
            data = np.array(img)
            alpha = data[:, :, 3]
            unique_alphas = np.unique(alpha)
            print(f"  RGBA image! Unique alphas: {unique_alphas[:10]}... (total {len(unique_alphas)})")
            transparent_count = np.sum(alpha == 0)
            opaque_count = np.sum(alpha == 255)
            semi_count = np.sum((alpha > 0) & (alpha < 255))
            total = img.size[0] * img.size[1]
            print(f"  Pixels: transparent={transparent_count} ({transparent_count/total*100:.25f}%), opaque={opaque_count} ({opaque_count/total*100:.2f}%), semi={semi_count} ({semi_count/total*100:.2f}%)")
        else:
            print("  Not RGBA.")
    else:
        print(f"{name} not found at {path}")
