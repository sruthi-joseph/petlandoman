import os
import shutil

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

shutil.copy2(os.path.join(image_dir, "banner_for_pet_products.jpeg"), os.path.join(artifact_dir, "banner_products.jpeg"))
shutil.copy2(os.path.join(image_dir, "banner_for_pet_services.jpeg"), os.path.join(artifact_dir, "banner_services.jpeg"))
print("Copied banners to artifact directory.")
