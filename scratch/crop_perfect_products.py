from PIL import Image, ImageDraw
import os

# Source JPEG images and their destination names
products = [
    ("pet food.jpeg", "product_1.png"),
    ("toys & fun.jpeg", "product_2.png"),
    ("groomin products.jpeg", "product_3.png"),
    ("accessories.jpeg", "product_4.png")
]

os.makedirs("extracted_images", exist_ok=True)

# Perfect circle geometry (centered on 2400x1792 canvas)
center_x, center_y = 1200, 892
outer_radius = 845  # Radius of the circle in the raw JPEGs
inner_radius = 835  # Reduce radius slightly to trim off the black border outline

for idx, (src_name, dest_name) in enumerate(products):
    if not os.path.exists(src_name):
        print(f"Warning: {src_name} not found, skipping.")
        continue
        
    print(f"Processing {src_name}...")
    img = Image.open(src_name).convert("RGBA")
    
    # 1. Crop to the square bounding box of the circular region
    box = (
        center_x - outer_radius,
        center_y - outer_radius,
        center_x + outer_radius,
        center_y + outer_radius
    )
    cropped = img.crop(box)
    
    # 2. Create a clean circular mask to crop out the black background and black border
    mask = Image.new("L", (outer_radius * 2, outer_radius * 2), 0)
    draw = ImageDraw.Draw(mask)
    
    # Draw white circle of inner_radius centered on the cropped canvas
    mask_center = outer_radius
    mask_box = (
        mask_center - inner_radius,
        mask_center - inner_radius,
        mask_center + inner_radius,
        mask_center + inner_radius
    )
    draw.ellipse(mask_box, fill=255)
    
    # 3. Apply the mask as the alpha channel
    cropped.putalpha(mask)
    
    # 4. Resize to high-resolution 500x500 for optimal sharpness/clarity on high-DPI screens
    final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
    
    # 5. Save the processed PNG
    final_img.save(f"extracted_images/{dest_name}")
    print(f"Saved extracted_images/{dest_name} successfully.")

print("All products processed successfully!")
