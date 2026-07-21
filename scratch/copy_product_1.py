import os
import shutil

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

shutil.copy2(os.path.join(image_dir, "product_1.png"), os.path.join(artifact_dir, "product_1.png"))
print("Copied product_1.png to artifacts.")
