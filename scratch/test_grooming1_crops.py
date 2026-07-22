from PIL import Image, ImageDraw
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\grooming-products1.jpeg"
im = Image.open(img_path).convert("RGBA")

# Let's test radii R = 850, 880, 890 with center (1200, 896)
center_x = 1200
center_y = 896

for r in [800, 850, 880, 890]:
    box = (center_x - r, center_y - r, center_x + r, center_y + r)
    cropped = im.crop(box)
    
    mask = Image.new("L", (r * 2, r * 2), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, r * 2, r * 2), fill=255)
    
    cropped.putalpha(mask)
    final_img = cropped.resize((500, 500), Image.Resampling.LANCZOS)
    final_img.save(f"c:\\Users\\SRUTHI\\Desktop\\petland oman\\scratch\\product_3_r{r}.png")
    print(f"Saved product_3_r{r}.png")
