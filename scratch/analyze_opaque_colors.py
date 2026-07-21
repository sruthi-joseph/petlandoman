from PIL import Image
import numpy as np
from collections import Counter
import os

def analyze_opaque_colors(path):
    name = os.path.basename(path)
    if not os.path.exists(path):
        print(f"{name} does not exist")
        return
    with Image.open(path) as img:
        img_rgba = img.convert("RGBA")
        arr = np.array(img_rgba)
        pixels = arr.reshape(-1, 4)
        # Filter for pixels that are mostly opaque (alpha > 128)
        opaque_pixels = pixels[pixels[:, 3] > 128]
        if len(opaque_pixels) == 0:
            print(f"{name} has no opaque pixels")
            return
        
        # Count dominant colors (convert to tuple of RGB)
        rgb_tuples = [tuple(p[:3]) for p in opaque_pixels]
        counter = Counter(rgb_tuples)
        most_common = counter.most_common(10)
        
        print(f"Dominant colors in OPAQUE pixels of {name} (out of {len(rgb_tuples)} pixels):")
        for color, count in most_common:
            percent = count / len(rgb_tuples) * 100
            print(f"  RGB {color}: {count} pixels ({percent:.1f}%)")

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
analyze_opaque_colors(os.path.join(folder, "img_4_R15.png"))
analyze_opaque_colors(os.path.join(folder, "img_0_R21.png"))
analyze_opaque_colors(r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\logo_transparent.png")
