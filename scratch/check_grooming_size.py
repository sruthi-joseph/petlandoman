from PIL import Image
import os

path = r"c:\Users\SRUTHI\Desktop\petland oman\grooming services.jpeg"
if os.path.exists(path):
    img = Image.open(path)
    print(f"Grooming services flyer dimensions: {img.size}")
else:
    print("Flyer not found at", path)
