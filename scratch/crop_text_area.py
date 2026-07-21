import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

img = Image.open(os.path.join(image_dir, "product_1.png"))
# Let's crop X=200 to 360, Y=130 to 180 (the text area)
crop = img.crop((200, 130, 360, 180))
crop.save(os.path.join(artifact_dir, "text_area_crop.png"))
print("Saved text_area_crop.png")
