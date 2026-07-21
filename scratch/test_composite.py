import os
from PIL import Image
import numpy as np

def test_composite(img_path, bg_color):
    with Image.open(img_path) as img:
        img_rgba = img.convert("RGBA")
        bg = Image.new("RGBA", img.size, bg_color)
        composited = Image.alpha_composite(bg, img_rgba).convert("RGB")
        
        # Get bounding box of original
        bbox = img.getbbox()
        if bbox:
            cropped = composited.crop(bbox)
            arr = np.array(cropped)
            avg_color = arr.mean(axis=(0, 1))
            print(f"Composited {img_path} over {bg_color} (cropped size {cropped.size}):")
            print(f"  Average RGB: {avg_color}")
            # Count pixels that are near-white (all channels > 240)
            white_pixels = np.sum(np.all(arr > 240, axis=-1))
            total = arr.shape[0] * arr.shape[1]
            print(f"  White-ish pixels (>240): {white_pixels} ({white_pixels/total*100:.1f}%)")
            # Count pixels that are near-black (all channels < 20)
            black_pixels = np.sum(np.all(arr < 20, axis=-1))
            total = arr.shape[0] * arr.shape[1]
            print(f"  Black-ish pixels (<20): {black_pixels} ({black_pixels/total*100:.1f}%)")

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
test_composite(os.path.join(folder, "img_4_R15.png"), (255, 255, 255, 255))
test_composite(os.path.join(folder, "img_4_R15.png"), (252, 194, 3, 255)) # yellow
