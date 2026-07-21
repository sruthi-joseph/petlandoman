import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

img = Image.open(os.path.join(image_dir, "banner_for_pet_products.jpeg"))
# Crop the bottom part
crop = img.crop((0, 750, img.width, img.height))
crop.save(os.path.join(artifact_dir, "banner_bottom_crop.png"))
print("Saved banner_bottom_crop.png")
