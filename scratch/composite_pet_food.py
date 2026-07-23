import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def segment_bag(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    from PIL import ImageDraw
    temp_img = img.copy()
    ImageDraw.floodfill(temp_img, (0, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, 0), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (0, h - 1), (0, 0, 0, 0), thresh=10)
    ImageDraw.floodfill(temp_img, (w - 1, h - 1), (0, 0, 0, 0), thresh=10)
    alpha = temp_img.split()[3]
    bbox = alpha.getbbox()
    if bbox:
        cropped = img.crop(bbox)
        mask = alpha.crop(bbox)
        # Apply erosion to the mask to remove any white fringe
        import scipy.ndimage as ndimage
        mask_arr = np.array(mask) > 0
        eroded = ndimage.binary_erosion(mask_arr, iterations=1)
        clean_mask = Image.fromarray((eroded * 255).astype(np.uint8))
        cropped.putalpha(clean_mask)
        return cropped
    return None

# Load the source high-res image
src_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
if not os.path.exists(src_path):
    print("Error: pet food.jpeg not found!")
    exit(1)

canvas = Image.open(src_path).convert("RGBA")
w_canvas, h_canvas = canvas.size

# Load and segment the three product bags
hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

bag_left = segment_bag(hairball_path)
bag_center = segment_bag(maxi_path)
bag_right = segment_bag(kitten_path)

# Optimized layout parameters
h_c = 1140
h_s = 855
dx = 298
y_c_bottom = 1346
y_s_bottom = 1346

w_c = int(bag_center.width * (h_c / bag_center.height))
w_l = int(bag_left.width * (h_s / bag_left.height))
w_r = int(bag_right.width * (h_s / bag_right.height))

# Resize bags with high quality
resized_left = bag_left.resize((w_l, h_s), Image.Resampling.LANCZOS)
resized_center = bag_center.resize((w_c, h_c), Image.Resampling.LANCZOS)
resized_right = bag_right.resize((w_r, h_s), Image.Resampling.LANCZOS)

# Create a clean background image inside the circle
circle_cx, circle_cy = 1200, 906
inner_radius = 764

# Create the mask for the circle interior
mask = Image.new("L", (w_canvas, h_canvas), 0)
draw = ImageDraw.Draw(mask)
draw.ellipse((circle_cx - inner_radius, circle_cy - inner_radius, 
              circle_cx + inner_radius, circle_cy + inner_radius), fill=255)
# Soft feather of 1px to blend edges perfectly
mask = mask.filter(ImageFilter.GaussianBlur(1))

# Create a solid color image for the background inside the circle
bg_color = (248, 234, 207, 255)  # RGB matching the clean background
circle_bg = Image.new("RGBA", (w_canvas, h_canvas), bg_color)

# Draw the three bags onto the clean circle background
# Layer 1: Left and Right bags
circle_bg.alpha_composite(resized_left, (circle_cx - dx - w_l // 2, y_s_bottom - h_s))
circle_bg.alpha_composite(resized_right, (circle_cx + dx - w_r // 2, y_s_bottom - h_s))

# Layer 2: Center bag (in front)
circle_bg.alpha_composite(resized_center, (circle_cx - w_c // 2, y_c_bottom - h_c))

# Composite the modified circle area onto the original canvas using the circular mask
final_canvas = Image.composite(circle_bg, canvas, mask)

# Convert back to RGB and save as JPEG to match original format
final_img = final_canvas.convert("RGB")
dest_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
final_img.save(dest_path, "JPEG", quality=95)

print(f"Successfully updated: {dest_path}")
