import os
import numpy as np
from PIL import Image, ImageChops

def segment_product(img_path):
    # Load image and convert to RGBA
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    
    # We will flood-fill the background with transparent color.
    # The background is white (255, 255, 255). We start flood fill from the corners:
    # (0, 0), (w-1, 0), (0, h-1), (w-1, h-1)
    # PIL's ImageDraw has floodfill, but we can also use PIL's Image.floodfill (available in newer Pillow versions)
    # or scipy/skimage, or do a simple BFS flood fill in Python.
    # Let's do a fast flood fill using scipy/ndimage or a simple python BFS (since it's fast enough for 1300x1300 if written cleanly).
    # Wait, we can use PIL's ImageDraw.floodfill! Let's check if it exists.
    # Yes, from PIL import ImageDraw; ImageDraw.floodfill(img, (0, 0), (0, 0, 0, 0), thresh=15)
    # Let's write a script to test this.
    temp_img = img.copy()
    from PIL import ImageDraw
    
    # Floodfill from four corners
    try:
        ImageDraw.floodfill(temp_img, (0, 0), (0, 0, 0, 0), thresh=10)
        ImageDraw.floodfill(temp_img, (w - 1, 0), (0, 0, 0, 0), thresh=10)
        ImageDraw.floodfill(temp_img, (0, h - 1), (0, 0, 0, 0), thresh=10)
        ImageDraw.floodfill(temp_img, (w - 1, h - 1), (0, 0, 0, 0), thresh=10)
    except Exception as e:
        print(f"Error during floodfill: {e}")
        return None
        
    # Now the alpha channel of temp_img will have 0 where background was filled,
    # and 255 where the product is (and possibly some white parts of the product are still 255).
    # Let's extract the alpha channel to get the product mask
    alpha = temp_img.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        product_cropped = img.crop(bbox)
        mask_cropped = alpha.crop(bbox)
        # Apply the mask to make background transparent
        product_cropped.putalpha(mask_cropped)
        return product_cropped
    return None

# Let's test on the primary images:
test_files = [
    ("HAIRBALL_26297", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"),
    ("KITTEN_36812", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36812.webp"),
    ("KITTEN_36813", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"),
    ("MAXI_25489", r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp")
]

os.makedirs(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\segmented", exist_ok=True)

for name, path in test_files:
    if os.path.exists(path):
        prod = segment_product(path)
        if prod:
            out_p = f"c:\\Users\\SRUTHI\\Desktop\\petland oman\\scratch\\segmented\\{name}.png"
            prod.save(out_p, "PNG")
            print(f"Segmented {name} -> size: {prod.size}")
        else:
            print(f"Failed to segment {name}")
    else:
        print(f"File not found: {path}")
