from PIL import Image
import os

files = ["logo.png", "logo_transparent.png", "logo_white_transparent.png"]
dir_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"

for f in files:
    path = os.path.join(dir_path, f)
    if os.path.exists(path):
        with Image.open(path) as img:
            print(f"{f}: format={img.format}, size={img.size}, mode={img.mode}")
    else:
        print(f"{f} does not exist")
