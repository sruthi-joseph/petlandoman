import os
from PIL import Image

highres_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
if os.path.exists(highres_path):
    img = Image.open(highres_path).convert("RGB")
    print(f"High-res image size: {img.size}")
    # Inspect center, left and right of the circle
    # Center: (1200, 906)
    # Left: (800, 906)
    # Right: (1600, 906)
    print("  (1200, 906):", img.getpixel((1200, 906)))
    print("  (800, 906):", img.getpixel((800, 906)))
    print("  (1600, 906):", img.getpixel((1600, 906)))
    print("  (1200, 1300) (bottom area):", img.getpixel((1200, 1300)))
else:
    print("Highres image not found!")
