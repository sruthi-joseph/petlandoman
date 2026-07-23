from PIL import Image, ImageDraw
import os

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food-home.jpeg"
dest_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_1.png"

im = Image.open(img_path).convert("RGBA")
w, h = im.size

# Detected circle parameters from scan
cx, cy = 1199.5, 907.5
r = 767.5

# Crop to enclosing box
box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
cropped = im.crop(box)

# Create high-res mask for anti-aliased smooth edges
mask_size = int(r * 2)
factor = 4
mask_large = Image.new("L", (mask_size * factor, mask_size * factor), 0)
draw_large = ImageDraw.Draw(mask_large)
draw_large.ellipse((0, 0, mask_size * factor, mask_size * factor), fill=255)

# Resize mask to crop size (downsample to mask_size)
mask = mask_large.resize(cropped.size, Image.Resampling.LANCZOS)
cropped.putalpha(mask)

# Resize to final size 500x500
final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)

# Save to destination
os.makedirs(os.path.dirname(dest_path), exist_ok=True)
final_img.save(dest_path, "PNG")
print(f"Saved smooth anti-aliased image to {dest_path}")
