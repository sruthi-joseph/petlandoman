from PIL import Image, ImageDraw
import os

# Define the coordinates and safe radii for each product image
products = [
    {
        "src": "pet food.jpeg",
        "dest": "product_1.png",
        "cx": 1200,
        "cy": 894,
        "r": 815
    },
    {
        "src": "toys & fun.jpeg",
        "dest": "product_2.png",
        "cx": 1200,
        "cy": 894,
        "r": 770
    },
    {
        "src": "groomin products.jpeg",
        "dest": "product_3.png",
        "cx": 1200,
        "cy": 901,
        "r": 740
    },
    {
        "src": "accessories.jpeg",
        "dest": "product_4.png",
        "cx": 1200,
        "cy": 896,
        "r": 865
    }
]

os.makedirs("extracted_images", exist_ok=True)

for p in products:
    src_name = p["src"]
    dest_name = p["dest"]
    cx, cy, r = p["cx"], p["cy"], p["r"]
    
    if not os.path.exists(src_name):
        print(f"Warning: {src_name} not found, skipping.")
        continue
        
    print(f"Processing {src_name} (center: {cx}, {cy}, radius: {r})...")
    img = Image.open(src_name).convert("RGBA")
    
    # Crop to a square box that contains the circle of radius r
    box = (
        cx - r,
        cy - r,
        cx + r,
        cy + r
    )
    cropped = img.crop(box)
    
    # Create a circular mask of the same size
    mask = Image.new("L", (r * 2, r * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, r * 2, r * 2), fill=255)
    
    # Apply mask
    cropped.putalpha(mask)
    
    # Resize to 500x500 for high resolution
    final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
    
    # Save the processed image
    final_img.save(f"extracted_images/{dest_name}")
    print(f"Saved extracted_images/{dest_name}")

print("All products processed successfully!")
