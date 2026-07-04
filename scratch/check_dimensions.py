import os
from PIL import Image

folder = r"c:\Users\SRUTHI\Desktop\petland oman\product card images"
files = ["pet food.jpeg", "toy &fun.jpeg", "grooming.jpeg", "accessories.jpeg"]

for f in files:
    path = os.path.join(folder, f)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"File: {f} | Dimensions: {img.size}")
    else:
        print(f"File {f} not found")
