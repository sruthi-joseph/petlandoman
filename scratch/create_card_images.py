import os
from PIL import Image

products = [
    ("pet food.jpeg", "card_prod_food.jpg"),
    ("toys & fun.jpeg", "card_prod_toys.jpg"),
    ("groomin products.jpeg", "card_prod_grooming.jpg"),
    ("accessories.jpeg", "card_prod_accessories.jpg")
]

base_dir = r"c:\Users\SRUTHI\Desktop\petland oman"
dest_dir = os.path.join(base_dir, "extracted_images")
os.makedirs(dest_dir, exist_ok=True)

# Geometry
center_x, center_y = 1200, 892
radius = 845

for src_name, dest_name in products:
    src_path = os.path.join(base_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"Warning: {src_name} not found")
        continue
        
    print(f"Processing {src_name}...")
    img = Image.open(src_path).convert("RGB")
    
    # Bounding box of the circular region (containing illustration + black bg)
    box = (
        center_x - radius,
        center_y - radius,
        center_x + radius,
        center_y + radius
    )
    cropped = img.crop(box)
    
    # Resize to 600x600 for sharp card display
    final_img = cropped.resize((600, 600), Image.Resampling.LANCZOS)
    
    # Save as compressed JPEG
    final_img.save(dest_path, "JPEG", quality=85)
    print(f"Saved {dest_path} successfully (size: {os.path.getsize(dest_path)} bytes)")

print("All card images processed!")
