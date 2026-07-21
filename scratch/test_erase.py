import os
from PIL import Image

image_dir = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images"
artifact_dir = r"C:\Users\SRUTHI\.gemini\antigravity-ide\brain\689489d0-f3a8-4c2f-95ed-ac5a20f36fb5"

img = Image.open(os.path.join(image_dir, "product_1.png")).convert("RGBA")
w, h = img.size

# We will erase the text in X: 208 to 352, Y: 138 to 170
# Let's sample the background colors at Y=135 and Y=173
y_top = 135
y_bottom = 173

pixels = img.load()

# Make a copy to edit
edited_img = img.copy()
edited_pixels = edited_img.load()

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
        
        edited_pixels[x, y] = (r, g, b, a)

edited_img.save(os.path.join(artifact_dir, "erased_text.png"))
print("Saved erased_text.png")
