import os
from PIL import Image
import numpy as np

img_names = ["svc_nutritional_final.png", "svc_training_final.png", "svc_grooming_final.png", "svc_daycare_final.png"]
base_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"

for name in img_names:
    path = os.path.join(base_dir, name)
    if not os.path.exists(path):
        print(f"{name} not found!")
        continue
    img = Image.open(path)
    print(f"\nImage: {name}")
    print(f"  Format: {img.format}, Size: {img.size}, Mode: {img.mode}")
    # check transparency / alpha channel
    if img.mode == "RGBA":
        alpha = np.array(img.split()[-1])
        unique_alphas = np.unique(alpha)
        print(f"  Alpha values: {len(unique_alphas)} unique values, min: {unique_alphas.min()}, max: {unique_alphas.max()}")
        opaque_pct = np.mean(alpha == 255) * 100
        transparent_pct = np.mean(alpha == 0) * 100
        semi_pct = 100 - opaque_pct - transparent_pct
        print(f"  Opaque: {opaque_pct:.1f}%, Transparent: {transparent_pct:.1f}%, Semi-transparent: {semi_pct:.1f}%")
    else:
        print("  No alpha channel (not RGBA)")
