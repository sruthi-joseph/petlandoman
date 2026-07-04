import os
from PIL import Image

base_dir = r"c:\Users\SRUTHI\Desktop\petland oman\service card images"
for name in sorted(os.listdir(base_dir)):
    path = os.path.join(base_dir, name)
    try:
        img = Image.open(path)
        print(f"File: {name} | Size: {img.size} | Format: {img.format} | Mode: {img.mode}")
    except Exception as e:
        print(f"Error {name}: {e}")
