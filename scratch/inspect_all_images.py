import os
from PIL import Image

base_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
for name in sorted(os.listdir(base_dir)):
    path = os.path.join(base_dir, name)
    if os.path.isdir(path):
        continue
    try:
        img = Image.open(path)
        print(f"File: {name} | Format: {img.format} | Size: {img.size} | Mode: {img.mode}")
    except Exception as e:
        print(f"Error reading {name}: {e}")
