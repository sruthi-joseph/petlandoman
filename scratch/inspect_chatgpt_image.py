import os
from PIL import Image

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\chatgpt_image_jun24.png"
if os.path.exists(p):
    with Image.open(p) as img:
        print(f"chatgpt_image_jun24.png: size={img.size}, mode={img.mode}, format={img.format}")
else:
    print("chatgpt_image_jun24.png not found")
