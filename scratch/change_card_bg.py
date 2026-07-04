import os
from PIL import Image, ImageDraw

src_dir = r"c:\Users\SRUTHI\Desktop\petland oman\service card images"
dest_dir = r"c:\Users\SRUTHI\Desktop\petland oman\extracted_images"
os.makedirs(dest_dir, exist_ok=True)

image_mapping = {
    "nutritional consulting.jpeg": "card_nutritional_opt.jpg",
    "obedience training.jpeg": "card_obedience_opt.jpg",
    "spa grooming.jpeg": "card_grooming_opt.jpg",
    "pet daycare & play.jpeg": "card_daycare_opt.jpg"
}

TARGET_COLOR = (252, 194, 3) # #FCC203
target_width = 800
target_height = 446

print("Replacing background with exact #FCC203 yellow:")
for src_name, dest_name in image_mapping.items():
    src_path = os.path.join(src_dir, src_name)
    dest_path = os.path.join(dest_dir, dest_name)
    
    if not os.path.exists(src_path):
        print(f"  Source not found: {src_name}")
        continue
        
    img = Image.open(src_path).convert("RGB")
    w, h = img.size
    
    # We will perform flood fill from the 4 corners: (0,0), (w-1,0), (0,h-1), (w-1,h-1)
    # This will fill the outer yellow background with exact #FCC203.
    # thresh=30 allows tolerance for JPEG artifacts.
    corners = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    
    for corner in corners:
        # We use ImageDraw.floodfill
        # It updates the image in place
        ImageDraw.floodfill(img, corner, TARGET_COLOR, thresh=30)
        
    # Resize to optimized size
    resized_img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    resized_img.save(dest_path, "JPEG", quality=85, optimize=True)
    
    print(f"  Processed {src_name} -> {dest_name} (Saved to extracted_images)")

print("Done.")
