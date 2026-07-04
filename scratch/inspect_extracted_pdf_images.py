import os
from PIL import Image

output_dir = r"c:\Users\SRUTHI\Desktop\petland oman\scratch\extracted_pdf_images"
for name in sorted(os.listdir(output_dir)):
    path = os.path.join(output_dir, name)
    try:
        img = Image.open(path)
        print(f"File: {name} | Size: {img.size} | Format: {img.format} | Mode: {img.mode}")
    except Exception as e:
        print(f"Error {name}: {e}")
