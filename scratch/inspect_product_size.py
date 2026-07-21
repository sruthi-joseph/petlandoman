import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
img = Image.open(os.path.join(image_dir, "product_1.png"))
print(f"product_1.png size: {img.size}, mode: {img.mode}")
