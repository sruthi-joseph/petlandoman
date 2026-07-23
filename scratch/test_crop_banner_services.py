from PIL import Image, ImageDraw
import os

p = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\landing banner-pet services.png"
img = Image.open(p).convert("RGBA")

# Bounding box coordinates:
# X=[31, 2061], Y=[35, 700]
# Width = 2061 - 31 + 1 = 2030
# Height = 700 - 35 + 1 = 666
box = (31, 35, 2061, 700)
cropped = img.crop(box)
w_c, h_c = cropped.size

# Create a rounded rectangle mask
radius = 70
factor = 4
mask_large = Image.new("L", (w_c * factor, h_c * factor), 0)
draw_large = ImageDraw.Draw(mask_large)
draw_large.rounded_rectangle((0, 0, w_c * factor, h_c * factor), radius * factor, fill=255)

mask = mask_large.resize((w_c, h_c), Image.Resampling.LANCZOS)
cropped.putalpha(mask)

# Save test image to scratch
cropped.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\test_banner_services.png", "PNG")
print("Saved test_banner_services.png")
