import os
import shutil
from PIL import Image, ImageDraw, ImageFont

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
img_path = os.path.join(image_dir, "product_1.png")
backup_path = os.path.join(image_dir, "product_1_backup_paweect.png")

# 1. Create backup
print("1. Creating backup of product image...")
shutil.copy2(img_path, backup_path)
print(f"Backup created at: {backup_path}")

# 2. Modify image in place
print("\n2. Erasing old text from bag...")
img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Image dimensions: {w}x{h}")

# We will erase the text in X: 208 to 352, Y: 138 to 170
# Sample background colors at Y=135 and Y=173
y_top = 135
y_bottom = 173

pixels = img.load()
for x in range(208, 353):
    color_top = pixels[x, y_top]
    color_bottom = pixels[x, y_bottom]
    
    # Linear interpolation for each row y from 136 to 172
    for y in range(136, 173):
        weight_bottom = (y - y_top) / (y_bottom - y_top)
        weight_top = 1.0 - weight_bottom
        
        r = int(color_top[0] * weight_top + color_bottom[0] * weight_bottom)
        g = int(color_top[1] * weight_top + color_bottom[1] * weight_bottom)
        b = int(color_top[2] * weight_top + color_bottom[2] * weight_bottom)
        a = int(color_top[3] * weight_top + color_bottom[3] * weight_bottom)
        
        pixels[x, y] = (r, g, b, a)

print("\n3. Rendering new text 'ROYAL CANIN'...")
# Text drawing setup
draw = ImageDraw.Draw(img)
text_color = (80, 48, 24, 255)
center_x = 280
center_y = 152

# Load Arial Bold font
font_path = "arialbd.ttf"
font_size = 21
font = ImageFont.truetype(font_path, font_size)

# Calculate position to center the text
bbox = draw.textbbox((0, 0), "ROYAL CANIN", font=font)
text_w = bbox[2] - bbox[0]
text_h = bbox[3] - bbox[1]

x = center_x - text_w // 2
y = center_y - text_h // 2

# Draw text
draw.text((x, y), "ROYAL CANIN", font=font, fill=text_color)
print(f"Rendered text at position ({x}, {y}) using Arial Bold 21pt")

# Save in-place
img.save(img_path, format="PNG")
print(f"Saved modified product image to: {img_path}")
