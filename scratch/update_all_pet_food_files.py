import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

highres_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\pet food.jpeg"
card_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet food.jpeg"
card_ref_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"

# 1. Check files presence
for p in [highres_path, card_path, card_ref_path]:
    if not os.path.exists(p):
        print(f"Error: {p} not found!")
        exit(1)

# Load images
img_high = Image.open(highres_path).convert("RGBA")
img_card = Image.open(card_path).convert("RGBA")
img_card_ref = Image.open(card_ref_path).convert("RGBA")

# Geometry of highres circle
hcx, hcy = 1200, 906
hr = 770 # outer edge of golden border

# Crop high-res circle area
crop_box = (hcx - hr, hcy - hr, hcx + hr, hcy + hr)
circle_crop = img_high.crop(crop_box)

# Mask for high-res circle (so only the circle itself is pasted)
circle_mask = Image.new("L", (hr * 2, hr * 2), 0)
draw_mask = ImageDraw.Draw(circle_mask)
draw_mask.ellipse((0, 0, hr * 2, hr * 2), fill=255)
# Soften edge
circle_mask = circle_mask.filter(ImageFilter.GaussianBlur(1))

# Apply mask to high-res circle crop
circle_crop.putalpha(circle_mask)

# Geometry of card circle
# Proportions: scale is approx 307 / 770 = 0.3987
ccx, ccy = 835, 475
cr = 307

# Resize high-res circle to match card circle size
circle_resized = circle_crop.resize((cr * 2, cr * 2), Image.Resampling.LANCZOS)

# Paste onto card images
def paste_circle_to_card(card_img):
    # Paste centered at (ccx, ccy)
    # The box is (ccx - cr, ccy - cr, ccx + cr, ccy + cr)
    p_box = (ccx - cr, ccy - cr, ccx + cr, ccy + cr)
    card_img.paste(circle_resized, p_box, circle_resized)
    return card_img.convert("RGB")

updated_card = paste_circle_to_card(img_card)
updated_card_ref = paste_circle_to_card(img_card_ref)

# Save card images
updated_card.save(card_path, "JPEG", quality=95)
print(f"Saved: {card_path}")
updated_card_ref.save(card_ref_path, "JPEG", quality=95)
print(f"Saved: {card_ref_path}")

# 2. Regenerate assets/images/extracted_images/product_1.png
# Same crop settings: cx=1200, cy=906, r=815. Masked and resized to 500x500
prod_r = 815
prod_box = (hcx - prod_r, hcy - prod_r, hcx + prod_r, hcy + prod_r)
prod_crop = img_high.crop(prod_box)

prod_mask = Image.new("L", (prod_r * 2, prod_r * 2), 0)
draw_prod_mask = ImageDraw.Draw(prod_mask)
draw_prod_mask.ellipse((0, 0, prod_r * 2, prod_r * 2), fill=255)
prod_crop.putalpha(prod_mask)

product_1_img = prod_crop.resize((500, 500), Image.Resampling.LANCZOS)
prod_1_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\extracted_images\product_1.png"
os.makedirs(os.path.dirname(prod_1_path), exist_ok=True)
product_1_img.save(prod_1_path, "PNG")
print(f"Saved: {prod_1_path}")

# 3. Regenerate assets/images/extracted_images/card_prod_food_new.png
# Crop card from card_ref_path using apply_pet_food_swap.py logic
# Detect yellow border region in updated_card_ref
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
print("All files updated and synchronized successfully!")
