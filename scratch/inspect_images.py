from PIL import Image
import os

folder = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_images"
files = sorted(os.listdir(folder))

for f in files:
    path = os.path.join(folder, f)
    try:
        with Image.open(path) as img:
            print(f"{f}: format={img.format}, size={img.size}, mode={img.mode}")
    except Exception as e:
        print(f"Error opening {f}: {e}")
