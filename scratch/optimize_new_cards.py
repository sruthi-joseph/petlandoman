import os
from PIL import Image

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\service card images"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
os.makedirs(dest_dir, exist_ok=True)

image_mapping = {
    "nutritional consulting.jpeg": "card_nutritional_opt.jpg",
    "obedience training.jpeg": "card_obedience_opt.jpg",
    "spa grooming.jpeg": "card_grooming_opt.jpg",
    "pet daycare & play.jpeg": "card_daycare_opt.jpg"
}

# Web-optimized target width, height maintains aspect ratio (1.79)
target_width = 800
target_height = 446

print("Optimizing Service Card Images:")
for src_name, dest_name in image_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"  Source not found: {src_name}")
        continue
        
    img = Image.open(src_path)
    # Resize using high-quality Lanczos resampling
    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    # Save as optimized JPEG (quality=85)
    resized_img.convert("RGB").save(dest_path, "JPEG", quality=85, optimize=True)
    
    orig_size_mb = os.path.getsize(src_path) / (1024 * 1024)
    opt_size_kb = os.path.getsize(dest_path) / 1024
    print(f"  Optimized {src_name} -> {dest_name}")
    print(f"    Original Size: {orig_size_mb:.2f} MB | Optimized Size: {opt_size_kb:.1f} KB")
