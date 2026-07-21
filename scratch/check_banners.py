import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images"
banners = ["banner_for_pet_products.jpeg", "banner_for_pet_services.jpeg"]

for name in banners:
    path = os.path.join(image_dir, name)
    if os.path.exists(path):
        img = Image.open(path)
        print(f"{name}: size={img.size}, mode={img.mode}, format={img.format}")
    else:
        print(f"{name} does not exist")
