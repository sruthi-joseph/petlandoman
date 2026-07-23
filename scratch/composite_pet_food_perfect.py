import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

def segment_and_cut_shadow(path, y_bottom_crop):
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
    if not bbox:
        return None
    x_min, y_min, x_max, y_max = bbox
    cropped_img = img.crop((x_min, y_min, x_max, y_bottom_crop))
    cropped_alpha = alpha.crop((x_min, y_min, x_max, y_bottom_crop))
    
    # Erode to clean up edges
    import scipy.ndimage as ndimage
    mask_arr = np.array(cropped_alpha) > 0
    eroded = ndimage.binary_erosion(mask_arr, iterations=1)
    clean_mask = Image.fromarray((eroded * 255).astype(np.uint8))
    cropped_img.putalpha(clean_mask)
    return cropped_img

# Load high-res canvas
src_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
# Load original high-res template (re-reading from backup if it exists, or just read the current file.
# Since we didn't touch the outside of the circle, we can read the current file.)
canvas = Image.open(src_path).convert("RGBA")
w_canvas, h_canvas = canvas.size

# Load and segment the three product bags
hairball_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\HAIRBALL\26297.webp"
maxi_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\MAXI\25489.webp"
kitten_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_list\pet food\KITTEN\36813.webp"

bag_left = segment_and_cut_shadow(hairball_path, 1163)
bag_center = segment_and_cut_shadow(maxi_path, 1166)
bag_right = segment_and_cut_shadow(kitten_path, 1230)

# Optimized layout parameters
h_c = 1130
h_s = 847
dx = 327
y_c_bottom = 1346
y_s_bottom = 1321

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
print(f"Successfully saved clean highres: {dest_path}")

# Run Synchronization for Cards and Extracted Images
card_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
card_ref_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"

# Load card templates
img_card = Image.open(card_path).convert("RGBA")
img_card_ref = Image.open(card_ref_path).convert("RGBA")

# Geometry of highres circle
hr = 770 # outer edge of golden border
crop_box = (circle_cx - hr, circle_cy - hr, circle_cx + hr, circle_cy + hr)
circle_crop = final_canvas.crop(crop_box)

circle_mask = Image.new("L", (hr * 2, hr * 2), 0)
draw_mask = ImageDraw.Draw(circle_mask)
draw_mask.ellipse((0, 0, hr * 2, hr * 2), fill=255)
circle_mask = circle_mask.filter(ImageFilter.GaussianBlur(1))
circle_crop.putalpha(circle_mask)

# Geometry of card circle
ccx, ccy = 835, 475
cr = 307
circle_resized = circle_crop.resize((cr * 2, cr * 2), Image.Resampling.LANCZOS)

# Paste onto card templates
def paste_circle_to_card(card_img):
    p_box = (ccx - cr, ccy - cr, ccx + cr, ccy + cr)
    card_img.paste(circle_resized, p_box, circle_resized)
    return card_img.convert("RGB")

updated_card = paste_circle_to_card(img_card)
updated_card_ref = paste_circle_to_card(img_card_ref)

updated_card.save(card_path, "JPEG", quality=95)
print(f"Saved: {card_path}")
updated_card_ref.save(card_ref_path, "JPEG", quality=95)
print(f"Saved: {card_ref_path}")

# Regenerate assets/images/extracted_images/product_1.png
prod_r = 815
prod_box = (circle_cx - prod_r, circle_cy - prod_r, circle_cx + prod_r, circle_cy + prod_r)
prod_crop = final_canvas.crop(prod_box)

prod_mask = Image.new("L", (prod_r * 2, prod_r * 2), 0)
draw_prod_mask = ImageDraw.Draw(prod_mask)
draw_prod_mask.ellipse((0, 0, prod_r * 2, prod_r * 2), fill=255)
prod_crop.putalpha(prod_mask)

product_1_img = prod_crop.resize((500, 500), Image.Resampling.LANCZOS)
prod_1_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_1.png"
product_1_img.save(prod_1_path, "PNG")
print(f"Saved: {prod_1_path}")

# Regenerate assets/images/extracted_images/card_prod_food_new.png
data_card = np.array(updated_card_ref)
r, g, b = data_card[:,:,0], data_card[:,:,1], data_card[:,:,2]
yellow_mask = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(yellow_mask)

dest_png = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\card_prod_food_new.png"
target_w = 800
target_h = 446
radius = 40

if len(xs) > 0 and len(ys) > 0:
    x_min, x_max = xs.min(), xs.max()
    y_min, y_max = ys.min(), ys.max()
    cropped_card = updated_card_ref.convert("RGB").crop((x_min, y_min, x_max + 1, y_max + 1))
else:
    cropped_card = updated_card_ref.convert("RGB")

src_w, src_h = cropped_card.size
target_ratio = target_w / target_h
src_ratio = src_w / src_h

if src_ratio > target_ratio:
    new_w = int(target_ratio * src_h)
    offset = (src_w - new_w) // 2
    cropped_ratio = cropped_card.crop((offset, 0, offset + new_w, src_h))
else:
    new_h = int(src_w / target_ratio)
    offset = (src_h - new_h) // 2
    cropped_ratio = cropped_card.crop((0, offset, src_w, offset + new_h))

resized_card = cropped_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)
alpha_mask = Image.new("L", (target_w, target_h), 0)
draw_alpha = ImageDraw.Draw(alpha_mask)
draw_alpha.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)
resized_card.putalpha(alpha_mask)

resized_card.save(dest_png, "PNG")
print(f"Saved: {dest_png}")
print("Synchronization complete!")
