import os
from PIL import Image

src_folder = r"c:\Users\SRUTHI\Desktop\petland oman\product card images"
dest_folder = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
os.makedirs(dest_folder, exist_ok=True)

files = [
    ("pet food.jpeg", "card_prod_food_opt.jpg"),
    ("toy &fun.jpeg", "card_prod_toys_opt.jpg"),
    ("grooming.jpeg", "card_prod_grooming_opt.jpg"),
    ("accessories.jpeg", "card_prod_accessories_opt.jpg")
]

target_size = (800, 446)

for src_name, dest_name in files:
    src_path = os.path.join(src_folder, src_name)
    dest_path = os.path.join(dest_folder, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Error: {src_path} not found")
        continue
        
    print(f"Resizing {src_name} to {target_size}...")
    img = Image.open(src_path).convert("RGB")
    resized = img.resize(target_size, Image.Resampling.LANCZOS)
    resized.save(dest_path, "JPEG", quality=85)
    print(f"Saved {dest_path} successfully (size: {os.path.getsize(dest_path)} bytes)")

print("All product card images optimized!")
