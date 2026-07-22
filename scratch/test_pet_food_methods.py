from PIL import Image, ImageDraw
import numpy as np

img_path = r"c:\Users\SRUTHI\Desktop\petland oman\assets\images\product_card_images\pet_food card.jpeg"
im = Image.open(img_path).convert("RGB")

target_w = 800
target_h = 446
radius = 40

# Method A: crop yellow card box
data = np.array(im)
r, g, b = data[:,:,0], data[:,:,1], data[:,:,2]
mask = (r > 175) & (g > 125) & (b < 130)
ys, xs = np.where(mask)
x_min, x_max = xs.min(), xs.max()
y_min, y_max = ys.min(), ys.max()
print(f"Yellow card box: X=[{x_min}, {x_max}], Y=[{y_min}, {y_max}]")

cropped = im.crop((x_min, y_min, x_max + 1, y_max + 1))
src_w, src_h = cropped.size
target_ratio = target_w / target_h
src_ratio = src_w / src_h

if src_ratio > target_ratio:
    new_w = int(target_ratio * src_h)
    offset = (src_w - new_w) // 2
    cropped_ratio = cropped.crop((offset, 0, offset + new_w, src_h))
else:
    new_h = int(src_w / target_ratio)
    offset = (src_h - new_h) // 2
    cropped_ratio = cropped.crop((0, offset, src_w, offset + new_h))

resized_a = cropped_ratio.resize((target_w, target_h), Image.Resampling.LANCZOS)
alpha_mask = Image.new("L", (target_w, target_h), 0)
draw = ImageDraw.Draw(alpha_mask)
draw.rounded_rectangle((0, 0, target_w, target_h), radius, fill=255)
resized_a.putalpha(alpha_mask)
resized_a.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\pet_food_method_a.png")

# Method B: direct resize & rounded mask
resized_b = im.resize((target_w, target_h), Image.Resampling.LANCZOS)
resized_b.putalpha(alpha_mask)
resized_b.save(r"c:\Users\SRUTHI\Desktop\petland oman\scratch\pet_food_method_b.png")

print("Both methods saved to scratch.")
