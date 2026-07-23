from PIL import Image, ImageDraw
import os

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food-home.jpeg"
im = Image.open(img_path).convert("RGBA")
w, h = im.size

# Detected circle parameters
cx, cy = 1199.5, 907.5
r = 767.5

# Let's crop to a square enclosing the circle
box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
cropped = im.crop(box)

# Now create a circular mask of the same size
mask_size = int(r * 2)
mask = Image.new("L", (mask_size, mask_size), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((0, 0, mask_size, mask_size), fill=255)

# Resize mask to crop size of the image just in case of rounding
cropped_mask = mask.resize(cropped.size, Image.Resampling.LANCZOS)
cropped.putalpha(cropped_mask)

# Resize to 500x500
final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
final_img.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\test_product_1.png", "PNG")
print("Saved scratch/test_product_1.png")
