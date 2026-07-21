from PIL import Image
import numpy as np
from collections import Counter
import os

def analyze_colors(path):
    name = os.path.basename(path)
    if not os.path.exists(path):
        print(f"{name} does not exist")
        return
    with Image.open(path) as img:
        img_rgba = img.convert("RGBA")
        arr = np.array(img_rgba)
        pixels = arr.reshape(-1, 4)
        # Filter out transparent pixels
        opaque_pixels = pixels[pixels[:, 3] > 10] # alpha > 10
        if len(opaque_pixels) == 0:
            print(f"{name} is fully transparent")
            return
        
        # Count dominant colors (convert to tuple of RGB)
        rgb_tuples = [tuple(p[:3]) for p in opaque_pixels]
        counter = Counter(rgb_tuples)
        most_common = counter.most_common(10)
        
        print(f"Dominant colors in {name} (out of {len(rgb_tuples)} non-transparent pixels):")
        for color, count in most_common:
            percent = count / len(rgb_tuples) * 100
            print(f"  RGB {color}: {count} pixels ({percent:.1f}%)")

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
analyze_colors(os.path.join(folder, "img_4_R15.png"))
analyze_colors(os.path.join(folder, "img_0_R21.png"))
analyze_colors(os.path.join(folder, "img_2_R18.png"))
