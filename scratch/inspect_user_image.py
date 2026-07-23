from PIL import Image
import os

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food-home.jpeg"
if os.path.exists(p):
    with Image.open(p) as img:
        print(f"File: {p}")
        print(f"Size: {img.size}")
        print(f"Mode: {img.mode}")
        print(f"Format: {img.format}")
else:
    print("File not found!")
