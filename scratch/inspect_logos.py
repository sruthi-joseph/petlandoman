import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
logos = ["logo.png", "logo_transparent.png", "logo_white_transparent.png"]

for name in logos:
    path = os.path.join(image_dir, name)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"{name}: size={img.size}, mode={img.mode}")
        bbox = img.getbbox()
        print(f"  bbox of non-zero pixels: {bbox}")
    else:
        print(f"{name} does not exist at {path}")
