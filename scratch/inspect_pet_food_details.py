import os
from PIL import Image

pet_food_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
if os.path.exists(pet_food_path):
    with Image.open(pet_food_path) as img:
        print(f"pet food.jpeg: size={img.size}, mode={img.mode}, format={img.format}")
else:
    print("pet food.jpeg not found!")

product_folders = {
    "HAIRBALL": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL",
    "KITTEN": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN",
    "MAXI": r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI"
}

for name, folder in product_folders.items():
    print(f"\nFolder: {name}")
    if os.path.exists(folder):
        for f in os.listdir(folder):
            fpath = os.path.join(folder, f)
            with Image.open(fpath) as img:
                print(f"  {f}: size={img.size}, mode={img.mode}, format={img.format}")
    else:
        print(f"  Folder not found: {folder}")
